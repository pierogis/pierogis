import math
import multiprocessing  as mp
import os
import time
from typing import Callable, List

import imageio

from .menu import menu
from .order import Order
from .ticket import Ticket
from .. import Pierogi, Dish


class Kitchen:
    menu = menu

    def __init__(self, chef, processes: int = None):
        self.chef = chef
        if processes is None:
            processes = os.cpu_count()
        self.processes = processes

    def __getstate__(self):
        self_dict = self.__dict__.copy()
        del self_dict['pool']
        return self_dict

    def __setstate__(self, state):
        self.__dict__.update(state)

    @staticmethod
    def cook_ticket(
            chef,
            ticket: Ticket
    ) -> None:
        """
        cook a ticket with a thread pool
        """
        dish = chef.assemble_ticket(ticket, menu)

        cooked_dish = chef.cook_dish(dish)

        cooked_dish.save(ticket.output_filename)

    def cook_tickets(self, tickets: List[Ticket], pool: mp.Pool = None, reader=None):
        """provide reader if you want to presave frames"""

        for ticket in tickets:
            if reader is not None:
                frame = reader.get_next_data()
                raw_dir = os.path.join('/tmp', 'raw')
                if not os.path.isdir(raw_dir):
                    os.makedirs(raw_dir)

                input_filename = os.path.join(raw_dir, os.path.basename(ticket.output_filename))
                writer = imageio.get_writer(input_filename)
                writer.append_data(frame)

                pierogi_desc = ticket.pierogis[ticket.base]
                ticket.files[pierogi_desc.files_key] = input_filename
                pierogi_desc.frame_index = 0

            if pool is not None:
                pool.apply_async(
                    func=self.cook_ticket,
                    args=(self.chef, ticket)
                )

            else:
                self.cook_ticket(self.chef, ticket)

    def _auto_pilot(self, order: Order, reader=None):
        """test some frames in the animation"""
        tickets = order.tickets

        # test with 5% of the frames, within 2 and 10
        pilot_frames = max(2, min(round(len(tickets) * .05), 10))

        next_frame_index = 0

        if len(tickets) > 8:
            frame_index = 0

            next_frame_index = frame_index + pilot_frames
            next_tickets = tickets[frame_index:next_frame_index]
            frame_index = next_frame_index

            # sync cooking
            start = time.perf_counter()
            self.cook_tickets(next_tickets)
            elapsed = time.perf_counter() - start

            next_frame_index = frame_index + pilot_frames
            next_tickets = tickets[frame_index:next_frame_index]
            frame_index = next_frame_index

            # sync cooking with presave frames
            presave_start = time.perf_counter()
            self.cook_tickets(next_tickets, reader=reader)
            presave_elapsed = time.perf_counter() - presave_start

            if presave_elapsed < elapsed:
                order.presave = True

                pool = mp.Pool()

                next_frame_index = frame_index + pilot_frames
                next_tickets = tickets[frame_index:next_frame_index]
                frame_index = next_frame_index

                # async cooking with presave frames
                async_presave_start = time.perf_counter()

                self.cook_tickets(next_tickets, reader=reader, pool=pool)
                pool.close()
                pool.join()

                async_presave_elapsed = time.perf_counter() - async_presave_start

                if async_presave_elapsed < presave_elapsed:
                    order.cook_async = True

            else:
                order.presave = False

                # async cooking
                pool = mp.Pool()

                next_frame_index = frame_index + pilot_frames
                next_tickets = tickets[frame_index:next_frame_index]
                frame_index = next_frame_index

                async_start = time.perf_counter()
                self.cook_tickets(next_tickets, pool=pool)
                pool.close()
                pool.join()
                async_elapsed = time.perf_counter() - async_start

                if async_elapsed < elapsed:
                    order.cook_async = True

        return next_frame_index

    def queue_order(self, order: Order, start_callback: Callable, report_status: Callable):
        frames = len(order.tickets)

        digits = math.floor(math.log(frames, 10)) + 1

        cooked_dir = 'cooked'

        if frames > 0:
            if not os.path.isdir(cooked_dir):
                os.makedirs(cooked_dir)

        frame_index = 1

        for ticket in order.tickets:
            padded_frame_index = str(frame_index).zfill(digits)

            if frames > 1:
                output_filename = os.path.join(
                    cooked_dir,
                    order.order_name + '-' + padded_frame_index + '.png'
                )

                ticket.output_filename = output_filename

                if os.path.isfile(output_filename):
                    if order.resume:
                        continue
                    else:
                        os.remove(output_filename)
            else:
                output_filename = os.path.join(cooked_dir, order.order_name + '.png')

            ticket.output_filename = output_filename
            frame_index += 1

        start_callback()

        if os.path.isfile(order.input_path):
            reader = imageio.get_reader(order.input_path)
        else:
            reader = None

        report_status(order, status='preprocessing')

        processed_frame_index = self._auto_pilot(order, reader)

        if not order.presave:
            reader = None
        if order.cook_async:
            pool = mp.Pool()
        else:
            pool = None

        next_tickets = order.tickets[processed_frame_index:]

        report_status(order, status='cooking')

        self.cook_tickets(next_tickets, pool=pool, reader=reader)

        if pool is not None:
            pool.close()
            pool.join()

    def plate(
            self,
            order: Order
    ) -> str:
        """"""
        input_path = order.input_path
        order_name = order.order_name

        pierogis = []

        cooked_dir = 'cooked'

        for filename in sorted(os.listdir(cooked_dir)):
            input_path = os.path.join(cooked_dir, filename)
            pierogis.append(Pierogi.from_path(path=input_path, frame_index=0))

        dish = Dish(pierogis=pierogis)

        output_filename = order.output_filename
        fps = order.fps
        optimize = order.optimize
        frame_duration = order.duration

        if output_filename is None:
            if order_name is None:
                order_name = os.path.splitext(os.path.basename(input_path))[0]
            if dish.frames == 1:
                output_filename = order_name + '.png'
            else:
                output_filename = order_name + '.gif'

        dish.save(output_filename, optimize, duration=frame_duration, fps=fps)

        return output_filename
