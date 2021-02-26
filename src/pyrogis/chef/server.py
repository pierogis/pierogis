"""
parsing
"""
import argparse
import math
import os
import time
from typing import List

from PIL import UnidentifiedImageError

from .menu import menu
from .ticket import Ticket
from ..ingredients import Dish


class Server:
    menu = menu
    orders = {}

    def _create_parser(self):
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

        # add parser options for outputting as animation (gif)
        togo_parser = argparse.ArgumentParser(add_help=False)
        togo_parser.add_argument(
            '-o', '--output',
            help="path to save resulting image"
        )
        togo_parser.add_argument(
            '--duration',
            type=int,
            help="duration in ms"
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

        subparsers.add_parser('togo', parents=[base_parser, togo_parser], add_help=False)

        for command, menu_item in self.menu.items():
            # inherit the parent class arguments
            # and arguments specific to a subcommand
            menu_item_parser = subparsers.add_parser(
                command,
                parents=[base_parser, togo_parser, menu_item.get_parser()],
                add_help=False
            )

        return parser

    def take_orders(self, order_name: str, args: list) -> List[Ticket]:
        """
        use a chef to parse list of strings into Tickets
        """
        parser = self._create_parser()

        # parse the input args with the applicable arguments attached
        parsed = parser.parse_args(args)
        parsed_vars = vars(parsed)

        # need the path to use as input for some recipes
        # like opening files for ingredients
        input_path = parsed_vars.pop('path')

        # need to take out the things just used for cli/io stuff
        fps = parsed_vars.pop('fps')
        duration = parsed_vars.pop('duration')
        optimize = parsed_vars.pop('optimize')

        dish = Dish(path=input_path)

        self.orders[order_name] = {
            'duration': duration,
            'fps': fps,
            'optimize': optimize,
            'frames': dish.frames
        }

        # if plate is the order, just assemble the plate from files in path
        if parsed_vars['order'] == 'togo':
            return []

        tickets = self.write_tickets(order_name, input_path, parsed_vars)

        return tickets

    def write_tickets(self, order_id: str, input_path, parsed_vars):
        """

        """
        cooked_dir = os.path.join('cooked', order_id)
        if not os.path.isdir(cooked_dir):
            os.makedirs(cooked_dir)

        if os.path.isdir(input_path):
            tickets = self._write_dir_tickets(input_path, cooked_dir, parsed_vars)
        elif os.path.isfile(input_path):
            # can be a gif/vid or an image
            tickets = self._write_file_tickets(input_path, cooked_dir, parsed_vars)
        else:
            raise Exception('Bad path')

        return tickets

    def _write_dir_tickets(self, cooked_dir, parsed_vars):
        """
        write Ticket for each image in a directory
        """
        input_paths = [cooked_dir + '/' + filename for filename in os.listdir(cooked_dir)]

        # sort so we can gif in order
        input_paths.sort()

        # get default handler parameter attached to subparsers
        # function for handling a command's options
        generate_ticket = parsed_vars.pop('generate_ticket')

        tickets = []

        for input_path in input_paths:
            try:
                # set the file on the cooked pierogi based on the input path
                cooked_path = os.path.join(
                    cooked_dir,
                    os.path.splitext(os.path.basename(input_path))[0] + ".png"
                )

                ticket = Ticket()
                # create a dish description for the specified cli recipe
                ticket = generate_ticket(ticket, path=cooked_path, **parsed_vars)

                tickets.append(ticket)

            except UnidentifiedImageError:
                print("{} is not an image".format(input_path))

            except ValueError:
                print("{} is not an image".format(input_path))

            except IsADirectoryError:
                print("{} is a directory".format(input_path))

        return tickets

    def _write_file_tickets(self, input_file, cooked_dir, parsed_vars):
        """
        handle a single file

        can be a gif/video or a single image
        """
        # if the path is an image, it should be cooked solo
        # if it is a gif, it should be

        dish = Dish(file=input_file)

        digits = math.floor(math.log(dish.frames, 10)) + 1

        if dish.frames > 1:
            i = 1

            for pierogi in dish.pierogis:
                # make frame file names like frames/0001.png
                frame_path = os.path.join(cooked_dir, str(i).zfill(digits) + '.png')

                pierogi.save(frame_path)

                i += 1

            tickets = self._write_dir_tickets(cooked_dir, parsed_vars)

        else:
            cooked_path = os.path.join(
                cooked_dir,
                os.path.splitext(os.path.basename(input_file))[0] + ".png"
            )

            dish.pierogis[0].save(cooked_path)

            ticket = Ticket()

            # get default handler parameter attached to subparsers
            # function for handling a command's options
            generate_ticket = parsed_vars.pop('generate_ticket')

            tickets = [generate_ticket(ticket, path=cooked_path, **parsed_vars)]

        return tickets

    def plate(self, order_name: str):
        cooked_dir = os.path.join("cooked", str(order_name))
        cooked_frames = len(os.listdir(cooked_dir))

        while cooked_frames < self.orders[order_name]['frames']:
            time.sleep(1)

            paths = os.listdir(cooked_dir)
            cooked_frames = len(paths)

    def togo(self, order_id, output_filename):
        cooked_dir = os.path.join("cooked", str(order_id))

        duration = self.orders[order_id]['duration']
        if duration is not None:
            duration /= 1000

        fps = self.orders[order_id]['fps']
        optimize = self.orders[order_id]['optimize']

        dish = Dish(path=cooked_dir)

        output_path = os.path.join("cooked", output_filename)

        dish.save(output_path, optimize, duration=duration, fps=fps)
