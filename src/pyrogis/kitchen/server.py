"""
parsing
"""
import argparse
import math
import os
import time
from typing import List, Dict, Generator

from .kitchen import Kitchen
from .ticket import Ticket
from ..ingredients import Dish


class Server:
    order_tickets: Dict[str, List[Ticket]]

    def __init__(self, cooked_dir: str = 'cooked'):
        self.cooked_dir = cooked_dir
        self.order_tickets = {}

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
            default=25,
            type=int
        )
        togo_parser.add_argument(
            '--no-optimize',
            dest='optimize',
            default=True,
            action='store_false',
            help="duration in ms"
        )

        return togo_parser

    def take_orders(self, order_name: str, args: List[str], kitchen: Kitchen) -> None:
        """
        use a chef to parse list of strings into Tickets
        """

        parser = self._create_parser(kitchen.menu)

        # parse the input args with the applicable arguments attached
        parsed, unknown = parser.parse_known_args(args)
        parsed_vars = vars(parsed)

        # need the path to use as input for some recipes
        # like opening files for ingredients
        input_path = parsed_vars.pop('path')

        dish = Dish.from_path(path=input_path)

        # if plate is the order, just assemble the plate from files in path
        if parsed_vars['order'] == 'togo':
            self.togo(order_name, dish, unknown)
        else:
            for ticket in self.write_tickets(order_name, dish, parsed_vars):
                self.order_tickets[order_name].append(ticket)
                kitchen.cook_ticket(order_name, self.cooked_dir, ticket)

            while not self.check_cooked(order_name):
                time.sleep(1)

            self.togo(order_name, dish)

    def write_tickets(self, order_name: str, dish: Dish, parsed_vars) -> Generator[Ticket, None, None]:
        """
        create tickets from a list of pierogis and parsed vars
        """
        self.remove_order_dir(order_name)

        cooked_order_dir = os.path.join(self.cooked_dir, order_name)

        os.makedirs(cooked_order_dir)

        generate_ticket = parsed_vars.pop('generate_ticket')

        for pierogi in dish.pierogis:
            ticket = Ticket()
            ticket = generate_ticket(ticket, pierogi, **parsed_vars.copy())

            yield ticket

    def remove_order_dir(self, order_name: str):
        cooked_dir = os.path.join(self.cooked_dir, order_name)

        if os.path.isdir(cooked_dir):
            for file in os.listdir(cooked_dir):
                os.remove(os.path.join(cooked_dir, file))
            os.removedirs(cooked_dir)

    def check_cooked(self, order_name: str) -> int:
        cooked_order_dir = os.path.join(self.cooked_dir, str(order_name))
        if os.path.isdir(cooked_order_dir):
            cooked_tickets = len(os.listdir(cooked_order_dir))
        else:
            cooked_tickets = 0

        order_tickets = self.order_tickets.get(order_name)
        if order_tickets is not None:
            submitted_tickets = len(order_tickets)
        else:
            submitted_tickets = 0


        print("{} tickets cooked of {}".format(cooked_tickets, submitted_tickets), end='\r')
        return cooked_tickets == submitted_tickets

    def togo(
            self,
            order_name: str,
            dish: Dish,
            args: List[str] = None,
            output_filename=None,
            fps=None,
            optimize=None,
            frame_duration=None,
    ) -> str:
        """

        """
        if args is not None:
            parser = self._create_togo_parser()

            parsed_vars = vars(parser.parse_args(args))

            output_filename = parsed_vars.pop('output_filename')
            fps = parsed_vars.pop('fps')
            optimize = parsed_vars.pop('optimize')
            frame_duration = parsed_vars.pop('frame_duration')

        else:
            # prompt for vars
            pass

        if output_filename is None:
            if dish.frames == 1:
                output_filename = order_name + '.png'
            else:
                output_filename = order_name + '.gif'

        dish.save(output_filename, optimize, duration=frame_duration, fps=fps)

        return output_filename
