import argparse
import math
import os
import sys

from PIL import UnidentifiedImageError

from pyrogis import Dish, Pierogi
from .chef import Chef
from .chef.dish_description import DishDescription

chef = Chef()


def create_parser():
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
    # output
    base_parser.add_argument(
        '-o', '--output',
        help="path to save resulting image"
    )
    # quiet
    base_parser.add_argument(
        '-q', '--quiet',
        default=False, action='store_true',
        help="don't output the save location"
    )

    # add parser options for outputting as animation (gif)
    plate_parser = argparse.ArgumentParser(add_help=False)
    plate_parser.add_argument(
        '--duration',
        type=int,
        help="duration in ms"
    )
    plate_parser.add_argument(
        '--fps',
        default=25,
        type=int
    )
    plate_parser.add_argument(
        '--no-optimize',
        dest='optimize',
        default=True,
        action='store_false',
        help="duration in ms"
    )

    subparsers.add_parser('plate', parents=[base_parser, plate_parser], add_help=False)

    for command, menu_item in chef.menu.items():
        # inherit the parent class arguments
        # and arguments specific to a subcommand
        menu_item_parser = subparsers.add_parser(
            command,
            parents=[base_parser, plate_parser, menu_item.get_parser()],
            add_help=False
        )

        menu_item_parser.add_argument(
            '--frames',
            dest='plate',
            default=True, action='store_false',
            help="save as frames. 'output' is assumed to be a directory"
        )

    return parser


def parse_args(args: list):
    """
    use a chef to parse args into specified command
    """
    parser = create_parser()

    # parse the input args with the applicable arguments attached
    parsed = parser.parse_args(args)
    parsed_vars = vars(parsed)

    return parsed_vars


def parse_common(parsed_vars):
    # need the path to use as input for some recipes
    # like opening files for ingredients
    path = parsed_vars.pop('path')
    # need to take out output because it is just used for cli stuff
    output = parsed_vars.pop('output')

    # quiet flag lets you turn off print filename
    quiet = parsed_vars.pop('quiet')

    return path, output, quiet


def cook_dish(path: str, add_dish_desc, parsed_vars):
    """
    create and cook the specified dish with the vars

    :param path: path to use for the media in the dish
    :param add_dish_desc: chef method used to handle the parsed_vars
    :param parsed_vars: arguments to the recipe to create
    """
    dish_desc = DishDescription()
    # create a dish description for the specified cli recipe
    dish_desc = add_dish_desc(dish_desc, path=path, **parsed_vars)

    # cook the generated description
    return chef.cook_dish_desc(dish_desc)


def plate(path, output, parsed_vars):
    duration = parsed_vars.pop('duration')
    if duration is not None:
        duration /= 1000

    fps = parsed_vars.pop('fps')
    optimize = parsed_vars.pop('optimize')

    if os.path.isdir(path):
        frames = os.listdir(path)
        # sort so we can gif in order
        frames.sort()

        pierogis = []

        for frame in frames:
            try:
                pierogis.append(Pierogi(file=os.path.join(path, frame)))

            except UnidentifiedImageError:
                print("{} is not an image".format(frame))

            except ValueError:
                print("{} is not an image".format(frame))

            except IsADirectoryError:
                print("{} is a directory".format(path))

        dish = Dish(pierogis=pierogis)

        if output is None:
            output = "cooked.gif"

    else:
        dish = Dish(file=path)

        if output is None:
            output = "cooked.png"

    print("plating '{}' to '{}'".format(path, output))

    dish.save(output, optimize, duration=duration, fps=fps)


def cook_dir(path, output, parsed_vars):
    """
    handle directory input

    plate order will not process the files, just save them collected

    other orders will be processed by the chef
    """
    paths = [path + '/' + filename for filename in os.listdir(path)]

    # sort so we can gif in order
    paths.sort()

    if output is None:
        output = "cooked"
    if not os.path.isdir(output):
        os.makedirs(output)

    # get default handler parameter attached to subparsers
    # function for handling a command's options
    add_dish_desc = parsed_vars.pop('add_dish_desc')

    for path in paths:
        try:
            # set the file on the cooked pierogi based on the input path
            output_filename = os.path.join(
                output,
                os.path.splitext(os.path.basename(path))[0] + ".png"
            )

            print("cooking '{}' to '{}'".format(path, output_filename), end='\r')

            # make a separate dish for each path
            cooked_dish = cook_dish(path, add_dish_desc, parsed_vars)

            cooked_dish.save(output_filename)

        except UnidentifiedImageError:
            print("{} is not an image".format(path))

        except ValueError:
            print("{} is not an image".format(path))

        except IsADirectoryError:
            print("{} is a directory".format(path))

    return output


def cook_file(path, output, parsed_vars):
    """
    handle a single file

    can be a gif/video or a single image
    """
    # if the path is an image, it should be cooked solo
    # if it is a gif, it should be
    dish = Dish(file=path)

    # get default handler parameter attached to subparsers
    # function for handling a command's options
    add_dish_desc = parsed_vars.pop('add_dish_desc')

    # input file is a video
    if len(dish.pierogis) > 1:
        if parsed_vars.get('plate'):
            frames_path = "cooked"
        elif output is None:
            frames_path = "cooked"
        else:
            frames_path = output

        if not os.path.isdir(frames_path):
            os.makedirs(frames_path)

        digits = math.floor(math.log(len(dish.pierogis), 10)) + 1

        i = 1
        for pierogi in dish.pierogis:
            # make frame file names like 0001.png
            frame_path = os.path.join(frames_path, str(i).zfill(digits) + '.png')

            print("cooking frame '{}' to '{}'".format(i, frame_path), end='\r')
            pierogi.save(frame_path)
            cooked_dish = cook_dish(frame_path, add_dish_desc, parsed_vars)
            cooked_dish.save(frame_path)

            i += 1

        if parsed_vars.get('plate'):
            plate(frames_path, output, parsed_vars)

    else:
        if output is None:
            output = "cooked.png"

        print("cooking '{}' to '{}'".format(path, output))

        cooked_dish = cook_dish(path, add_dish_desc, parsed_vars)

        cooked_dish.pierogis[0].file = path
        cooked_dish.save(output)

    return output


def main(args=None):
    """cli program"""
    if args is None:
        args = sys.argv[1:]

    parsed_vars = parse_args(args)

    input_path, output, quiet = parse_common(parsed_vars)

    # if plate is the order, just assemble the plate from files in path
    if parsed_vars['order'] == 'plate':
        plate(input_path, output, parsed_vars)

    else:
        if os.path.isdir(input_path):
            # if the path given contains many media
            if parsed_vars.get('plate'):
                frames_path = cook_dir(input_path, None, parsed_vars)
                plate(frames_path, output, parsed_vars)
            else:
                output_path = cook_dir(input_path, output, parsed_vars)

        elif os.path.isfile(input_path):
            # can be a gif/vid or an image
            frames_path = cook_file(input_path, output, parsed_vars)

        else:
            raise Exception('Bad path')

if __name__ == "__main__":
    sys.exit(main())
