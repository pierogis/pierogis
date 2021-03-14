"""
parsing
"""
import argparse
import math
import os
import time
from typing import List, Generator

from rich.progress import Progress

from .kitchen import Kitchen
from .order import Order
from .ticket import Ticket
from ..ingredients import Dish


class Server:
    orders: List[Order]

    @property
    def order_names(self):
        return [order.order_name for order in self.orders]

    def __init__(self, cooked_dir: str = 'cooked'):
        self.cooked_dir = cooked_dir
        self.orders = []

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

    def take_order(self, args: List[str], kitchen: Kitchen) -> List[str]:
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
        order_name = parsed_vars.pop('order_name')

        dish = Dish.from_path(path=input_path, order_name=order_name)

        output_filenames = []

        # if the order is just togo, don't need the kitchen
        if parsed_vars['order'] == 'togo':
            output_filename = self.togo(
                input_path=input_path,
                order_name=order_name,
                args=unknown,
                fps=dish.fps
            )
            output_filenames = [output_filename]
        else:
            if order_name is None:
                order_name = os.path.splitext(os.path.basename(input_path))[0]

            frames = dish.frames

            order = Order(order_name)

            frame_index = 1
            digits = math.floor(math.log(frames, 10)) + 1

            if frames > 0:
                if not os.path.isdir(self.cooked_dir):
                    os.makedirs(self.cooked_dir)

            order.fps = dish.fps

            with Progress() as progress:
                queue_ticket_task = progress.add_task('Queueing tickets...', total=frames)
                for ticket in self.write_tickets(dish, input_path, parsed_vars):
                    order.add_ticket(ticket)

                    if frames > 1:
                        padded_frame_index = str(frame_index).zfill(digits)

                        output_filename = os.path.join(
                            self.cooked_dir,
                            order_name + '-' + padded_frame_index + '.png'
                        )

                        if os.path.isfile(output_filename):
                            os.remove(output_filename)

                        frame_index += 1
                    else:
                        output_filename = os.path.join(self.cooked_dir, order_name + '.png')

                    kitchen.queue_ticket(output_filename, ticket)
                    output_filenames.append(output_filename)

                    progress.update(queue_ticket_task, advance=1, refresh=True)

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

    def check_order(self, order: Order, args: List[str]):
        """"""
        total = self.order_size(order)
        with Progress() as progress:
            cook_task = progress.add_task("[cyan]Cooking tickets...", total=total)
            while True:
                completed = self.cooked_tickets(order)
                progress.update(cook_task, completed=completed, refresh=True)

                if completed == total:
                    self.togo(args=args, order=order)
                    break
                else:
                    time.sleep(1)

    def togo(
            self,
            input_path: str = None,
            order: Order = None,
            args: List[str] = None,
            output_filename: str = None,
            fps: float = 25,
            optimize: bool = None,
            frame_duration: int = None,
    ) -> str:
        """

        """
        if input_path is None:
            input_path = self.cooked_dir

        dish = Dish.from_path(input_path, order.order_name)

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
            if order.order_name is None:
                order_name = os.path.splitext(os.path.basename(input_path))[0]
            if dish.frames == 1:
                output_filename = order.order_name + '.png'
            else:
                output_filename = order.order_name + '.gif'

        if fps is None:
            fps = order.fps

        dish.save(output_filename, optimize, duration=frame_duration, fps=fps)

        return output_filename
