"""
parsing
"""
import argparse
import math
import os
import time
from typing import List, Generator, Callable

from .kitchen import Kitchen
from .order import Order
from .ticket import Ticket
from ..ingredients import Dish


class Server:
    orders: List[Order]

    @property
    def order_names(self):
        return [order.order_name for order in self.orders]

    def __init__(
            self,
            cooked_dir: str = 'cooked',
            report_status: Callable = None,
            report_times: Callable = None
    ):
        self.cooked_dir = cooked_dir
        self.orders = []
        self.report_status = report_status
        self.report_times = report_times

    def _create_parser(self, menu):
        # create top level parser
        parser = argparse.ArgumentParser(
            description='** image processing pipelines **'
        )
        subparsers = parser.add_subparsers(
            dest='order', required=True
        )

        # create parent parser to pass down arguments only
        base_parser = argparse.ArgumentParser()
        base_parser.add_argument(
            'path',
            default='./',
            help="path to file or directory to use as input")
        base_parser.add_argument(
            '--order-name',
            help="path to file or directory to use as input")

        subparsers.add_parser('togo', parents=[base_parser], add_help=False)

        for command, menu_item in menu.items():
            # inherit the parent class arguments
            # and arguments specific to a subcommand
            subparsers.add_parser(
                command,
                parents=[base_parser, menu_item.get_parser()],
                add_help=False
            )

        return parser

    def _create_togo_parser(self):
        # add parser options for outputting as animation (gif)
        togo_parser = argparse.ArgumentParser(add_help=False)
        togo_parser.add_argument(
            '-o', '--output',
            dest='output_filename',
            help="path to save resulting image"
        )
        togo_parser.add_argument(
            '--frame-duration',
            type=int,
            help="frame duration in ms"
        )
        togo_parser.add_argument(
            '--fps',
            type=int,
            help="frames per second"
        )
        togo_parser.add_argument(
            '--no-optimize',
            dest='optimize',
            default=True,
            action='store_false',
            help="duration in ms"
        )

        return togo_parser

    def take_order(
            self, args: List[str], kitchen: Kitchen,
            report_times: Callable = None,
            report_status: Callable = None
    ) -> List[str]:
        """
        use a chef to parse list of strings into Tickets
        """

        togo_parser = self._create_togo_parser()
        parsed, unknown = togo_parser.parse_known_args(args)
        parsed_togo_vars = vars(parsed)

        parser = self._create_parser(kitchen.menu)
        # parse the input args with the applicable arguments attached
        parsed = parser.parse_args(unknown)
        parsed_vars = vars(parsed)

        # need the path to use as input for some recipes
        # like opening files for ingredients
        input_path = parsed_vars.pop('path')
        order_name = parsed_vars.pop('order_name')

        dish = Dish.from_path(path=input_path, order_name=order_name)

        output_filename = parsed_togo_vars.pop('output_filename')
        fps = parsed_togo_vars.pop('fps')
        optimize = parsed_togo_vars.pop('optimize')
        frame_duration = parsed_togo_vars.pop('frame_duration')

        if fps is None:
            fps = dish.fps

        order = Order(
            order_name,
            fps=fps,
            output_filename=output_filename,
            optimize=optimize,
            duration=frame_duration
        )

        output_filenames = []

        # when reading the input file is slower than saving an output frame, save the frames

        # if the order is just togo, don't need the kitchen
        if parsed_vars['order'] == 'togo':
            output_filename = self.togo(
                order=order,
                input_path=input_path,
            )
            output_filenames = [output_filename]
        else:
            if order.order_name is None:
                order.order_name = os.path.splitext(os.path.basename(input_path))[0]

            frames = dish.frames

            if report_status is not None:
                self.report_status(total=frames, description=order.order_name)

            def report_times(times):
                assembly_time = times[0]
                cook_time = times[1]
                save_time = times[2]

                assembly_times.append(assembly_time)

                total_cook_time = sum(times)

                alpha * total_cook_time + (1 - alpha) * self.cook_rate

                kitchen_progress.update(kitchen_task, refresh=False, cook_rate=cook_rate)

            frame_index = 1
            digits = math.floor(math.log(frames, 10)) + 1

            if frames > 0:
                if not os.path.isdir(self.cooked_dir):
                    os.makedirs(self.cooked_dir)

            queueing = False

            for ticket in self.write_tickets(dish, input_path, parsed_vars):
                order.add_ticket(ticket)

                padded_frame_index = str(frame_index).zfill(digits)
                if frames > 1:
                    output_filename = os.path.join(
                        self.cooked_dir,
                        order.order_name + '-' + padded_frame_index + '.png'
                    )
                else:
                    output_filename = os.path.join(self.cooked_dir, order.order_name + '.png')

                if os.path.isfile(output_filename):
                    os.remove(output_filename)

                frame_index += 1

                if frame_index < 10:
                    times = kitchen.cook_ticket(
                        kitchen.chef,
                        output_filename,
                        ticket
                    )

                    self.report_status(times)

                    if frame_index > 10 and order.cook_rate > 10:
                        if update_order_status is not None:
                            update_order_status(description='cooking')

                else:
                    if not queueing:
                        queueing = True
                        if update_order_status is not None:
                            update_order_status(description='queueing')

                    kitchen.queue_ticket(output_filename, ticket)

                output_filenames.append(output_filename)

            self.orders.append(order)

        return output_filenames

    def write_tickets(
            self, dish: Dish, input_path, parsed_vars
    ) -> Generator[Ticket, None, None]:
        """
        create tickets from a list of pierogis and parsed vars
        """
        generate_ticket = parsed_vars.pop('generate_ticket')

        for frame_index in range(len(dish.pierogis)):
            ticket = Ticket()
            ticket = generate_ticket(ticket, input_path, frame_index, **parsed_vars.copy())

            yield ticket

    def order_size(self, order: Order) -> int:
        order_tickets = order.tickets
        if order_tickets is not None:
            submitted_tickets = len(order_tickets)
        else:
            submitted_tickets = 0

        return submitted_tickets

    def cooked_tickets(self, order: Order):
        cooked_tickets = len(
            [
                filename for filename
                in os.listdir(self.cooked_dir)
                if filename.startswith(order.order_name)
            ]
        )

        return cooked_tickets

    def check_order(
            self,
            order: Order,
            timeout: float = 1200,
            update_callback=None
    ):

        """"""

        total = self.order_size(order)

        retries = 0
        wait_time = 1
        last_completed = None

        while True:
            completed = self.cooked_tickets(order)
            if update_callback is not None:
                if last_completed is not None:
                    order.smooth_cook_rate((completed - last_completed) / wait_time)
                    update_callback(completed=completed, cook_rate=order.cook_rate)
                else:
                    update_callback(completed=completed)

            if completed == total:
                success = True
                break
            # elif retries * wait_time > timeout:
            #     success = False
            #     break
            else:
                time.sleep(wait_time)

            last_completed = completed
            retries += 1

        return success

    def togo(
            self,
            order: Order,
            input_path: str = None,
    ) -> str:
        """"""
        if input_path is None:
            input_path = self.cooked_dir

        order_name = order.order_name

        dish = Dish.from_path(input_path, order_name)

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

        if fps is None:
            fps = order.fps

        dish.save(output_filename, optimize, duration=frame_duration, fps=fps)

        return output_filename
