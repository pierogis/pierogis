"""
parsing
"""
import argparse
import os
from typing import List

from .ticket import Ticket
from ..ingredients import Dish


class Server:
    orders = {}
    cooked_dir = 'cooked'

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

    def take_orders(self, order_name: str, args: List[str], menu: dict) -> List[Ticket]:
        """
        use a chef to parse list of strings into Tickets
        """

        parser = self._create_parser(menu)

        # parse the input args with the applicable arguments attached
        parsed, unknown = parser.parse_known_args(args)
        parsed_vars = vars(parsed)

        # need the path to use as input for some recipes
        # like opening files for ingredients
        input_path = parsed_vars.pop('path')

        dish = Dish.from_path(path=input_path)

        # if plate is the order, just assemble the plate from files in path
        if parsed_vars['order'] == 'togo':
            if args[0] == 'togo':
                parser = self._create_togo_parser()

            self.togo(order_name, dish, **vars(parser.parse_args(unknown)))
            return []
        else:
            tickets = self.write_tickets(order_name, dish, parsed_vars)

            return tickets

    def _write_dish_tickets(self, dish: Dish, parsed_vars: dict) -> List[Ticket]:
        generate_ticket = parsed_vars.pop('generate_ticket')

        tickets = []

        for pierogi in dish.pierogis:
            ticket = Ticket()
            ticket = generate_ticket(ticket, pierogi, parsed_vars.copy())

            tickets.append(ticket)

        return tickets

    def write_tickets(self, order_name: str, dish: Dish, parsed_vars):
        """
        create tickets from a list of pierogis and parsed vars
        """
        self.remove_order_dir(order_name)

        order_dir = os.path.join(self.cooked_dir, order_name)

        os.makedirs(order_dir)

        # could be async
        dish.save_frames(order_dir)

        tickets = self._write_dish_tickets(dish, parsed_vars)

        recipe_path = os.path.join(order_dir, 'recipe.json')

        return tickets

    @classmethod
    def remove_order_dir(cls, order_name: str):
        order_dir = os.path.join(cls.cooked_dir, order_name)
        if os.path.isdir(order_dir):
            for file in os.listdir(order_dir):
                os.remove(os.path.join(order_dir, file))
            os.removedirs(order_dir)

    def check(self, cooked_dir: str) -> int:
        paths = os.listdir(cooked_dir)
        return len(paths)

    def togo(self,
             order_name: str,
             dish: Dish,
             output_filename: str,
             fps: float,
             optimize: bool,
             frame_duration: float = None
             ) -> str:
        """

        """
        if frame_duration is not None:
            fps = 1000 / frame_duration

        if not os.path.isdir(self.cooked_dir):
            os.makedirs(self.cooked_dir)

        if output_filename is None:
            output_filename = order_name + '.gif'

        output_path = os.path.join(self.cooked_dir, output_filename)

        dish.save(output_path, optimize, fps=fps)

        return output_path
