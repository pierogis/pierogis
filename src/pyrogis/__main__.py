import argparse
import os
import sys

from PIL import UnidentifiedImageError

from .chef import Chef
from .chef.dish_description import DishDescription

chef = Chef()


def create_parser():
    # create top level parser
    parser = argparse.ArgumentParser(
        description='** image processing pipelines **'
    )
    subparsers = parser.add_subparsers(
        dest='recipe', required=True
    )

    # create parent parser to pass down arguments only
    parent_parser = argparse.ArgumentParser()
    parent_parser.add_argument(
        'path',
        default='./',
        help="path to file or directory to use as input")
    parent_parser.add_argument(
        '-o', '--output',
        default='./cooked',
        help="path and filename to save resulting image"
    )
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

    return parser


def parse_args(args: list):
    """
    use a chef to parse args into specified command
    """
    parser = create_parser()

    # parse the input args with the applicable arguments attached
    parsed = parser.parse_args(args)
    parsed_vars = vars(parsed)
    # need the path to use as input for some recipes
    # like opening files for ingredients
    path = parsed_vars.pop('path')
    # need to take out output because it is just used for cli stuff
    output = parsed_vars.pop('output')
    quiet = parsed_vars.pop('quiet')

    # get default handler parameter attached to subparsers
    # function for handling a command's options
    add_dish_desc = parsed_vars.pop('add_dish_desc')

    return path, output, quiet, parsed_vars, add_dish_desc


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


def main(args=None):
    """cli program"""
    if args is None:
        args = sys.argv[1:]

    path, output, quiet, parsed_vars, add_dish_desc = parse_args(args)

    # check if the path given contains many media
    if os.path.isdir(path):
        paths = [path + '/' + filename for filename in os.listdir(path)]
    elif os.path.isfile(path):
        paths = [path]
    else:
        raise Exception('Bad path')

    if not os.path.exists(output):
        os.makedirs(output)

    # loop through the potential media paths
    for path in paths:
        try:
            cooked_dish = cook_dish(path, add_dish_desc, parsed_vars)

            output_filename = os.path.join(
                output, os.path.split(path)[1]
            )

            if not quiet:
                print("Saving " + output_filename)

            # save to the outcome filename
            cooked_dish.save(output_filename)

        except UnidentifiedImageError:
            print("{} is not an image".format(path))

        except IsADirectoryError:
            print("{} is a directory".format(path))


if __name__ == "__main__":
    sys.exit(main())
