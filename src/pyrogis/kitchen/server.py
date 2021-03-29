"""
parsing
"""
import argparse
import os
import time
from threading import Thread
from typing import List, Callable

import imageio

from .kitchen import Kitchen
from .order import Order
from .ticket import Ticket


class Server:
    orders: List[Order]

    @property
    def order_names(self):
        return [order.order_name for order in self.orders]

    def __init__(
            self,
            report_status: Callable = None,
            # cooked_dir: str = 'cooked',
    ):
        # self.cooked_dir = cooked_dir
        self.orders = []
        self._report_status = report_status

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
            self, args: List[str], kitchen: Kitchen
    ) -> None:
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
        input_path = os.path.expanduser(parsed_vars.pop('path'))
        order_name = parsed_vars.pop('order_name')

        output_filename = parsed_togo_vars.pop('output_filename')
        fps = parsed_togo_vars.pop('fps')
        optimize = parsed_togo_vars.pop('optimize')
        frame_duration = parsed_togo_vars.pop('frame_duration')

        order = Order(
            order_name,
            input_path,
            fps=fps,
            output_filename=output_filename,
            optimize=optimize,
            duration=frame_duration
        )

        if order.fps is None:
            if os.path.isfile(input_path):
                order.fps = imageio.get_reader(input_path).get_meta_data()['fps']

        # if the order is just togo, don't need the kitchen
        if parsed_vars['order'] == 'togo':
            self.report_status(order, status='boxing')

            if os.path.isdir(input_path):
                # debug here
                for filename in sorted(os.listdir(input_path)):
                    if filename.startswith(order_name):
                        frame_path = os.path.join(input_path, filename)
                        ticket = Ticket(output_filename=frame_path)
                        order.add_ticket(ticket)
            else:
                for i in range(imageio.get_reader(input_path).count_frames()):
                    ticket = Ticket()
                    order.add_ticket(ticket)

            frames = len(order.tickets)
            self.report_status(order, total=frames)

            kitchen.plate(
                order=order,
                report_status=self.report_status
            )
        else:
            self.report_status(order, status='writing tickets')

            # order has tickets attached (for frames)
            self.write_tickets(order, parsed_vars)

            frames = len(order.tickets)
            self.report_status(order, total=frames)

            # the Server splits off part of their consciousness into a new thread
            check_thread = Thread(target=self.check_order, args=[order])

            def start_callback():
                check_thread.start()

            close_callback = kitchen.queue_order(order, start_callback, self.report_status)

            self.report_status(order, status='awaiting')
            close_callback()
            check_thread.join()

            self.report_status(order, status='plating')

            kitchen.plate(
                order,
                report_status=self.report_status
            )

        self.report_status(order, status='done')

    def write_tickets(
            self, order: Order, parsed_vars
    ) -> None:
        """
        create tickets from a list of pierogis and parsed vars
        """
        generate_ticket = parsed_vars.pop('generate_ticket')

        order_input_path = order.input_path
        order_name = order.order_name

        if os.path.isfile(order_input_path):
            reader = imageio.get_reader(order_input_path)
            frames = reader.count_frames()

            for frame_index in range(frames):
                ticket = Ticket()
                ticket = generate_ticket(ticket, order_input_path, frame_index, **parsed_vars.copy())

                order.add_ticket(ticket)

        elif os.path.isdir(order_input_path):
            # debug here
            for filename in sorted(os.listdir(order_input_path)):
                if filename.startswith(order_name):
                    input_path = os.path.join(
                        order_input_path,
                        filename
                    )

                    ticket = Ticket()
                    ticket = generate_ticket(ticket, input_path, 0, **parsed_vars.copy())

                    order.add_ticket(ticket)

    def order_size(self, order: Order) -> int:
        order_tickets = order.tickets
        if order_tickets is not None:
            submitted_tickets = len(order_tickets)
        else:
            submitted_tickets = 0

        return submitted_tickets

    def cooked_tickets(self, order: Order):
        cooked_tickets = 0
        for filename in order.output_filenames:
            if os.path.exists(os.path.join(filename)):
                cooked_tickets += 1

        return cooked_tickets

    def check_order(
            self,
            order: Order
    ):

        """"""

        total = self.order_size(order)

        retries = 0
        wait_time = 1

        while True:
            completed = self.cooked_tickets(order)

            self.report_status(
                order,
                completed=completed
            )

            if completed == total:
                break
            else:
                time.sleep(wait_time)

            retries += 1

    def report_status(self, order, **kwargs):
        if self._report_status is not None:
            self._report_status(order, **kwargs)
