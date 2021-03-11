"""
parsing
"""
import argparse
import os
import uuid
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

    def take_order(self, args: List[str], kitchen: Kitchen, order_name: str = None) -> List[str]:
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

        if order_name is None:
            order_name = uuid.uuid4().hex

        output_filenames = []

        # if the order is just togo, don't need the kitchen
        if parsed_vars['order'] == 'togo':
            self.order_tickets[order_name] = [Ticket() for i in range(dish.frames)]
            output_filenames = dish.save_frames(self.cooked_dir, order_name)
        else:
            frames = dish.frames

            self.order_tickets[order_name] = []

            frame_index = 1
            for ticket in self.write_tickets(dish, input_path, parsed_vars):
                self.order_tickets[order_name].append(ticket)

                if not os.path.isdir(self.cooked_dir):
                    os.makedirs(self.cooked_dir)

                if frames > 1:
                    output_filename = os.path.join(
                        self.cooked_dir,
                        order_name + '-' + str(frame_index) + '.png'
                    )

                    frame_index += 1
                else:
                    output_filename = os.path.join(self.cooked_dir, order_name + '.png')

                kitchen.queue_ticket(output_filename, ticket)
                output_filenames.append(output_filename)

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

    def check_order(self, order_name) -> int:
        cooked_tickets = len(
            [
                filename for filename
                in os.listdir(self.cooked_dir)
                if filename.startswith(order_name)
            ]
        )

        order_tickets = self.order_tickets.get(order_name)
        if order_tickets is not None:
            submitted_tickets = len(order_tickets)
        else:
            submitted_tickets = 0

        print("{} tickets cooked of {}".format(cooked_tickets, submitted_tickets), end='\r')
        return cooked_tickets == submitted_tickets

    def togo(
            self,
            input_path: str = None,
            order_name: str = None,
            args: List[str] = None,
            output_filename: str = None,
            fps: float = None,
            optimize: bool = None,
            frame_duration: int = None,
    ) -> str:
        """

        """
        if input_path is None:
            input_path = self.cooked_dir

        dish = Dish.from_path(input_path, order_name)

        if args is not None:
            parser = self._create_togo_parser()

            parsed_vars = vars(parser.parse_known_args(args)[0])

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
