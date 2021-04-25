import math
import multiprocessing as mp
import os
import signal
import sys
import tempfile
import time
from collections import defaultdict
from typing import Callable, List, Dict

import imageio

from . import menu
from .chef import Cooker
from .menu import Filling
from .order import Order
from .ticket import Ticket
from ..course import Course
from ..ingredients import Pierogi, Dish


def initializer():
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    sys.stdout = open(os.devnull, 'w')


class Kitchen:
    """cook a collection of Ticket objects"""
    menu: Dict[str, Filling] = menu.menu

    _pool: mp.Pool

    def _start_pool(self, processes: int):
        self.pool = mp.Pool(processes, initializer=initializer)

    def __init__(
            self,
            cooker: Cooker,
            cooked_dir: str = 'cooked',
            raw_dir: str = None
    ):
        """

        :param cooker:
                Chef-like object to cook with - can be anything that implements the base Chef's methods
        :param processes:
                number of cpus to use (defaults to os.cpu_count / 2)
        :param cooked_dir:
                to output cooked frames
        :param output_dir:
                dir to output fully cooked and plated courses to
        :param raw_dir:
                dir to store raw input files if necessary (defaults to tempfile.mkdtemp)
        """
        self.cooker = cooker
        self.pool = None
        self.cooked_dir = cooked_dir

        if raw_dir is None:
            raw_dir = tempfile.mkdtemp(suffix='raw')
        self.raw_dir = raw_dir

    def __getstate__(self):
        self_dict = self.__dict__.copy()
        del self_dict['pool']
        return self_dict

    def __setstate__(self, state):
        self.__dict__.update(state)

    @classmethod
    def cook_ticket(
            cls,
            cooker: Cooker,
            ticket: Ticket
    ) -> None:
        """cook a ticket with a thread pool"""
        dish = cooker.assemble_ticket(ticket, cls.menu)
        cooked_dish = cooker.cook_dish(dish)
        cooked_dish.pierogi.save(ticket.output_path)

    def _presave_ticket(self, frame, ticket: Ticket):
        if not os.path.isdir(self.raw_dir):
            os.makedirs(self.raw_dir)

        input_filename = os.path.join(self.raw_dir, os.path.basename(ticket.output_path))
        writer = imageio.get_writer(input_filename)
        writer.append_data(frame)

        pierogi_desc = ticket.pierogis[ticket.base]
        ticket.files[pierogi_desc.files_key] = input_filename
        pierogi_desc.frame_index = 0

    def _auto_pilot(self, order: Order) -> List[Ticket]:
        """test some frames in the animation"""
        tickets = [ticket for ticket in order.tickets if not ticket.skip]

        if len(order.tickets) > 8 and (order.presave is None or order.cook_async is None):
            # test with 5% of the frames, within 2 and 10
            seq_pilot_frames = 2

            frame_index = 0

            next_frame_index = frame_index + seq_pilot_frames
            next_tickets = tickets[frame_index:next_frame_index]
            frame_index = next_frame_index

            # sync cooking
            start = time.perf_counter()
            for ticket in next_tickets:
                self.cook_ticket(self.cooker, ticket)
            seq_rate = seq_pilot_frames / (time.perf_counter() - start)

            if order.presave is None:
                next_frame_index = frame_index + 2
                next_tickets = tickets[frame_index:next_frame_index]
                order.reader.set_image_index(next_tickets[0].pierogis[next_tickets[0].base].frame_index)
                frame_index = next_frame_index
                # sync cooking with presave frames
                presave_start = time.perf_counter()

                for ticket in next_tickets:
                    frame = order.reader.get_next_data()
                    self._presave_ticket(frame, ticket)
                    self.cook_ticket(self.cooker, ticket)

                presave_rate = seq_pilot_frames / (time.perf_counter() - presave_start)

                if presave_rate > seq_rate:
                    order.presave = True
                    seq_rate = presave_rate
                else:
                    order.presave = False

            if order.cook_async is None:
                par_pilot_frames = max(2, min(round(len(tickets) * .05), 10))

                if order.presave:
                    next_frame_index = frame_index + par_pilot_frames
                    next_tickets = tickets[frame_index:next_frame_index]
                    frame_index = next_frame_index

                    results = []

                    if self.pool is None:
                        self._start_pool(order.processes)

                    # async cooking with presave frames
                    par_presave_start = time.perf_counter()

                    for ticket in next_tickets:
                        frame = order.reader.get_next_data()
                        self._presave_ticket(frame, ticket)

                        def error_callback(exception: Exception):
                            order.failures.put((exception, ticket))

                        results.append(self.pool.apply_async(
                            self.cook_ticket, (self.cooker, ticket), error_callback=error_callback
                        ))

                    for result in results:
                        result.wait()

                    par_rate = par_pilot_frames / (time.perf_counter() - par_presave_start)

                else:
                    # parallel cooking

                    next_frame_index = frame_index + par_pilot_frames
                    next_tickets = tickets[frame_index:next_frame_index]
                    frame_index = next_frame_index

                    par_start = time.perf_counter()

                    results = []

                    if self.pool is None:
                        self._start_pool(order.processes)

                    for ticket in next_tickets:
                        def error_callback(exception: Exception):
                            order.failures.put((exception, ticket))

                        results.append(self.pool.apply_async(
                            self.cook_ticket, (self.cooker, ticket), error_callback=error_callback
                        ))

                    for result in results:
                        result.wait()

                    par_rate = par_pilot_frames / (time.perf_counter() - par_start)

                if par_rate > seq_rate:
                    order.cook_async = True

            next_tickets = tickets[frame_index:]

        else:
            next_tickets = tickets

        return next_tickets

    def _set_output_paths(self, order: Order):
        frames = len(order.tickets)

        digits = math.floor(math.log(frames, 10)) + 1

        cooked_dir = self.cooked_dir

        if not os.path.isdir(cooked_dir):
            os.makedirs(cooked_dir)

        suborders = defaultdict(list)

        for ticket in order.tickets:
            suborder_name = ticket.input_filename

            suborders[suborder_name].append(ticket)

        for suborder_name, suborder in suborders.items():
            suborder_length = len(suborder)

            frame_index = 0

            for ticket in suborder:
                if suborder_length > 1:
                    padded_frame_index = str(frame_index + 1).zfill(digits)
                    frame_suffix = '-' + padded_frame_index
                else:
                    frame_suffix = ''

                output_path = os.path.join(
                    cooked_dir,
                    '{suborder_base}{frame_suffix}{extension}'.format(
                        suborder_base=os.path.splitext(suborder_name)[0],
                        frame_suffix=frame_suffix,
                        extension='.png'
                    )
                )

                if os.path.isfile(output_path):
                    input_is_output = os.path.samefile(ticket.input_path, output_path)

                    # this is really rough and can be solved by a system
                    # for manipulating courses/animations as a whole
                    if order.resume:
                        ticket.skip = True
                    elif input_is_output:
                        if not os.path.isdir(self.raw_dir):
                            os.makedirs(self.raw_dir)

                        raw_input_path = os.path.join(
                            self.raw_dir, os.path.basename(ticket.input_path)
                        )
                        os.rename(ticket.input_path, raw_input_path)
                        ticket.input_path = raw_input_path
                    else:
                        os.remove(output_path)

                ticket.output_path = output_path
                frame_index += 1

    def queue_order(
            self, order: Order, report_status: Callable
    ):
        self._set_output_paths(order)

        report_status(order, status='preprocessing')

        if not os.path.isfile(order.input_path):
            order.presave = False

        next_tickets = self._auto_pilot(order)

        report_status(order, status='cooking')

        for ticket in next_tickets:
            if order.presave:
                next_frame_index = next_tickets[0].pierogis[next_tickets[0].base].frame_index
                if next_frame_index > 0:
                    order.reader.set_frame_index(next_frame_index)

                frame = order.reader.get_next_data()
                self._presave_ticket(frame, ticket)

            if order.cook_async:
                if self.pool is None:
                    self._start_pool(order.processes)

                def error_callback(exception: Exception):
                    order.failures.put((exception, ticket))

                self.pool.apply_async(
                    func=self.cook_ticket,
                    args=(self.cooker, ticket),
                    error_callback=error_callback
                )

            else:
                self.cook_ticket(self.cooker, ticket)

        if self.pool is not None:
            self.pool.close()
            self.pool.join()

    def plate(
            self,
            order: Order
    ) -> str:
        """"""
        dishes = []

        if len(order.tickets) == 0:
            raise Exception("Order has no tickets")

        for ticket in order.tickets:
            frame_path = ticket.output_path

            dish = Dish(pierogi=Pierogi.from_path(path=frame_path))

            dishes.append(dish)

        course = Course(dishes=dishes)

        fps = order.fps
        optimize = order.optimize
        frame_duration = order.duration
        audio_path = order.audio_path

        course.save(
            order.output_path,
            optimize=optimize,
            duration=frame_duration,
            fps=fps,
            audio_path=audio_path
        )

        return order.output_path
