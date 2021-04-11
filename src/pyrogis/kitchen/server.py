"""
parsing
"""
import argparse
import os
import time
from abc import abstractmethod
from threading import Thread
from typing import List, Callable, Protocol

import imageio

from .kitchen import Kitchen
from .order import Order
from .ticket import Ticket


class OrderTaker(Protocol):
    """any object that implements take_order and check_order is an OrderTaker"""

    @abstractmethod
    def take_order(
            self, args: List[str], kitchen: Kitchen
    ) -> Order:
        pass


class Server(OrderTaker):
    """handles tasks related to taking input and preparing it for Kitchen"""

    def __init__(
            self,
            report_callback: Callable = None,
    ):
        self._report_callback = report_callback

    def _create_parser(self, menu):
        # create top level parser
        parser = argparse.ArgumentParser(
            description='** image processing pipelines **'
        )
        subparsers = parser.add_subparsers(
            dest='filling', required=True
        )

        # create parent parser to pass down arguments only
        base_parser = argparse.ArgumentParser()
        base_parser.add_argument(
            'path',
            default='./',
            help="path to file or directory to use as input"
        )
        base_parser.add_argument(
            '--order-name',
            help="""
            name of order for filename prefixes; used to identify files for output
            """
        )

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
            dest='output_path',
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

    def _write_tickets(
            self, order: Order, parsed_vars
    ) -> None:
        """create tickets from a list of pierogis and parsed vars"""
        generate_ticket = parsed_vars.pop('generate_ticket')
        parsed_vars.pop('filling')

        input_path = order.input_path
        order_name = order.order_name

        if os.path.isfile(input_path):
            reader = imageio.get_reader(input_path)
            if hasattr(reader, 'count_frames'):
                frames = reader.count_frames()
            else:
                frames = len(reader)

            for frame_index in range(frames):
                ticket = Ticket()
                ticket = generate_ticket(ticket, input_path, frame_index, **parsed_vars.copy())

                order.add_ticket(ticket)

        elif os.path.isdir(input_path):
            # debug here
            filenames = [
                filename
                for filename
                in os.listdir(input_path)
                if filename != ".DS_Store"
            ]
            for filename in sorted(filenames):
                if order_name is None or filename.startswith(order_name):
                    ticket_input_path = os.path.join(
                        input_path,
                        filename
                    )

                    ticket = Ticket()
                    ticket = generate_ticket(ticket, ticket_input_path, 0, **parsed_vars.copy())

                    order.add_ticket(ticket)

        else:
            raise FileNotFoundError(input_path)

    def _handle_togo(self, order: Order):
        self._report_status(order, status='boxing')

        if os.path.isdir(order.input_path):
            # debug here
            filenames = [
                filename
                for filename
                in os.listdir(order.input_path)
                if filename != ".DS_Store"
            ]
            for filename in sorted(filenames):
                if order.order_name is None or filename.startswith(order.order_name):
                    frame_path = os.path.join(order.input_path, filename)
                    ticket = Ticket(output_path=frame_path)
                    order.add_ticket(ticket)
        else:
            for i in range(imageio.get_reader(order.input_path).count_frames()):
                ticket = Ticket()
                order.add_ticket(ticket)

        frames = len(order.tickets)
        self._report_status(order, total=frames)

    def _handle_filling(self, order: Order, parsed_vars: dict, kitchen: Kitchen):
        self._report_status(order, status='writing')

        presave = parsed_vars.pop('presave')
        cook_async = parsed_vars.pop('async')
        processes = parsed_vars.pop('processes')
        resume = parsed_vars.pop('resume')

        order.presave = presave
        order.cook_async = cook_async
        order.processes = processes
        order.resume = resume

        # order has tickets attached (for frames)
        self._write_tickets(order, parsed_vars)

        frames = len(order.tickets)
        self._report_status(order, total=frames)

        # the Server splits off part of their consciousness into a new thread
        check_thread = Thread(target=self._check_order, args=[order])
        check_thread.daemon = True

        # don't start the checker thread until the kitchen is ready
        def start_callback():
            check_thread.start()

        self._report_status(order, status='cooking')

        kitchen.queue_order(order, start_callback, self._report_status)
        check_thread.join()

        self._report_status(order, status='boxing')

    def take_order(
            self, args: List[str], kitchen: Kitchen
    ) -> Order:
        """
        take a list of args and turn it into an Order for the Kitchen
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

        output_path = parsed_togo_vars.pop('output_path')
        fps = parsed_togo_vars.pop('fps')
        optimize = parsed_togo_vars.pop('optimize')
        frame_duration = parsed_togo_vars.pop('frame_duration')

        order = Order(
            order_name, input_path,
            output_path=output_path,
            fps=fps,
            duration=frame_duration,
            optimize=optimize
        )

        if order.fps is None:
            if os.path.isfile(input_path):
                order.fps = imageio.get_reader(input_path).get_meta_data().get('fps')

        # if the order is just togo, don't need the kitchen
        if parsed_vars['filling'] == 'togo':
            self._handle_togo(order)
        else:
            self._handle_filling(order, parsed_vars, kitchen)

        kitchen.plate(
            order=order
        )

        self._report_status(order, status='done')

        return order

    @staticmethod
    def _count_cooked_tickets(order: Order) -> int:
        cooked_tickets = 0
        for filename in order.ticket_output_paths:
            if os.path.exists(os.path.join(filename)):
                cooked_tickets += 1

        return cooked_tickets

    def _check_order(
            self,
            order: Order
    ) -> int:
        """check and report how many tickets from an Order have been cooked"""
        total = len(order.tickets)

        wait_time = .1

        failed_output_paths = []

        while True:
            completed = self._count_cooked_tickets(order)

            while not order.failures.empty():
                exception, ticket = order.failures.get()
                failed_output_paths.append(ticket.output_path)

            self._report_status(
                order,
                completed=completed,
                branches=failed_output_paths
            )

            if completed + len(failed_output_paths) == total:
                break
            else:
                time.sleep(wait_time)

        return completed

    def _report_status(self, order, **kwargs) -> None:
        """
        currently pushes the status to a configured collback

        this could also log to a file
        """

        if self._report_callback is not None:
            self._report_callback(order, **kwargs)
