import argparse
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
    parent_parser = argparse.ArgumentParser()
    parent_parser.add_argument(
        'path',
        default='./',
        help="path to file or directory to use as input")
    # output
    parent_parser.add_argument(
        '-o', '--output',
        help="path to save resulting image"
    )
    # quiet
    parent_parser.add_argument(
        '-q', '--quiet',
        default=False, action='store_true',
        help="don't output the save location"
    )

    for command, menu_item in chef.menu.items():
        # inherit the parent class arguments
        # and arguments specific to a subcommand
        subparsers.add_parser(
            command,
            parents=[parent_parser, menu_item.get_parser()],
            add_help=False
        )

    plate_subparser = subparsers.add_parser(
        'plate',
        parents=[parent_parser],
        add_help=False
    )
    plate_subparser.add_argument(
        '-d', '--duration',
        type=int,
        help="duration in ms"
    )
    plate_subparser.add_argument(
        '-f', '--fps',
        default=25,
        type=int
    )
    plate_subparser.add_argument(
        '--no-optimize',
        dest='optimize',
        default=True,
        action='store_false'
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


def assemble(path, output, parsed_vars):
    frames = os.listdir(path)
    # sort so we can gif in order
    frames.sort()

    pierogis = []

    for frame in frames:
        try:
            pierogis.append(Pierogi(file=os.path.join(path, frame)))

        except UnidentifiedImageError:
            print("{} is not an image".format(path))

        except ValueError:
            print("{} is not an image".format(path))

        except IsADirectoryError:
            print("{} is a directory".format(path))

    dish = Dish(pierogis=pierogis)
    if output is None:
        output = "cooked.gif"
    duration = parsed_vars.pop('duration')
    if duration is not None:
        duration /= 1000
    fps = parsed_vars.pop('fps')
    optimize = parsed_vars.pop('optimize')
    dish.save(output, optimize, duration=duration, fps=fps)

    exit(0)


def cook_dir(path, output, parsed_vars):
    paths = [path + '/' + filename for filename in os.listdir(path)]

    # sort so we can gif in order
    paths.sort()

    if parsed_vars['order'] == 'plate':
        assemble(path, output, parsed_vars)

    if output is None:
        output = "cooked"
    if not os.path.isdir(output):
        os.makedirs(output)

    else:
        # get default handler parameter attached to subparsers
        # function for handling a command's options
        add_dish_desc = parsed_vars.pop('add_dish_desc')

        for path in paths:
            try:
                cooked_dish = cook_dish(path, add_dish_desc, parsed_vars)
                cooked_dish.pierogis[0].file = os.path.join(
                    output,
                    os.path.splitext(os.path.basename(path))[0] + ".png"
                )
                cooked_dish.save(output)

            except UnidentifiedImageError:
                print("{} is not an image".format(path))

            except ValueError:
                print("{} is not an image".format(path))

            except IsADirectoryError:
                print("{} is a directory".format(path))


def cook_file(path, output, parsed_vars):
    # if the path is an image, it should be cooked solo
    # if it is a gif, it should be
    dish = Dish(file=path)

    # get default handler parameter attached to subparsers
    # function for handling a command's options
    add_dish_desc = parsed_vars.pop('add_dish_desc')

    # input file is a video
    if len(dish.pierogis) > 1:
        if output is None:
            output = "cooked"
        if not os.path.isdir(output):
            os.makedirs(output)

        i = 1
        for pierogi in dish.pierogis:
            frame_path = os.path.join(output, str(i).zfill(4) + '.png')
            i += 1

            pierogi.save(frame_path)
            cooked_dish = cook_dish(frame_path, add_dish_desc, parsed_vars)
            cooked_dish.save(frame_path)

    else:
        cooked_dish = cook_dish(path, add_dish_desc, parsed_vars)
        if output is None:
            output = "cooked.png"
        cooked_dish.pierogis[0].file = path
        cooked_dish.save(output)


def main(args=None):
    """cli program"""
    if args is None:
        args = sys.argv[1:]

    parsed_vars = parse_args(args)

    path, output, quiet = parse_common(parsed_vars)

    if os.path.isdir(path):
        # if the path given contains many media
        cook_dir(path, output, parsed_vars)
    elif os.path.isfile(path):
        # can be a gif/vid or an image
        cook_file(path, output, parsed_vars)
    else:
        raise Exception('Bad path')


if __name__ == "__main__":
    sys.exit(main())
