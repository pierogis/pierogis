import math
import multiprocessing  as mp
import os
import time
from collections import Callable
from typing import Tuple

import imageio

from .menu import menu
from .order import Order
from .ticket import Ticket
from .. import Dish


class Kitchen:
    menu = menu

    def __init__(self, chef, report_times: Callable[Tuple[float, float, float]] = None):
        self.chef = chef
        self.pool = mp.Pool()

    @staticmethod
    def cook_ticket(
            chef, output_filename: str,
            ticket: Ticket
    ) -> Tuple[float, float, float]:
        """
        cook a ticket with a thread pool
        """
        assemble_start = time.perf_counter()
        dish = chef.assemble_ticket(ticket, menu)
        assemble_time = time.perf_counter() - assemble_start

        cook_start = time.perf_counter()
        cooked_dish = chef.cook_dish(dish)
        cook_time = time.perf_counter() - cook_start

        save_start = time.perf_counter()
        cooked_dish.save(output_filename)
        save_time = time.perf_counter() - save_start

        return assemble_time, cook_time, save_time

    def queue_order(self, order: Order):
        frames = len(order.tickets)

        digits = math.floor(math.log(frames, 10)) + 1

        frame_index = 1

        cooked_dir = 'cooked'

        if frames > 0:
            if not os.path.isdir(cooked_dir):
                os.makedirs(cooked_dir)

        reader = imageio.get_reader(order.input_path)

        for ticket in order.tickets:
            padded_frame_index = str(frame_index).zfill(digits)

            if frames > 1:
                output_filename = os.path.join(
                    cooked_dir,
                    order.order_name + '-' + padded_frame_index + '.png'
                )
            else:
                output_filename = os.path.join(cooked_dir, order.order_name + '.png')

            save_frames = False

            if os.path.isfile(output_filename):
                os.remove(output_filename)

            if save_frames:
                reader.set_frame_index(frame_index)
                frame = reader.get_next_data()
                writer = imageio.get_writer(output_filename)
                writer.write(frame)

                pierogi_desc = ticket.pierogis[ticket.base]
                pierogi_desc.files_key = output_filename
                pierogi_desc.frame_index = 0

            times = []

            def handler(result):
                times.append(result.get())

            cook_async = False

            if cook_async:
                self.pool.apply_async(
                    func=self.cook_ticket,
                    args=(self.chef, output_filename, ticket),
                    callback=handler
                )
            else:
                self.cook_ticket(self.chef, output_filename, ticket)

    def close(self):
        self.pool.close()

    def __getstate__(self):
        self_dict = self.__dict__.copy()
        del self_dict['pool']
        return self_dict

    def __setstate__(self, state):
        self.__dict__.update(state)

    def plate(
            self,
            order: Order
    ) -> str:
        """"""
        input_path = order.input_path
        order_name = order.order_name

        dish = self.chef.plate(input_path, order_name)

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
