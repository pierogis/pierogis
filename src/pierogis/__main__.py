import argparse
import os
import sys
import time

from .ingredients import Dish
from .chef import Chef


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    chef = Chef()

    # create top level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create parent parser to pass down arguments only
    parent_parser = argparse.ArgumentParser()
    parent_parser.add_argument('path', default='./')
    parent_parser.add_argument('-o', '--output', help='Path and filename to save resulting image')

    for command, command_parser in chef.menu.items():
        # inherit the parent class arguments and the arguments specific to a subcommand
        subparser = subparsers.add_parser(command, parents=[parent_parser, command_parser], add_help=False)

    parsed = parser.parse_args(args)
    parsed_vars = vars(parsed)
    path = parsed_vars.pop('path')
    output = parsed_vars.pop('output')

    if os.path.isdir(path):
        paths = [path + '/' + filename for filename in os.listdir(path)]
    elif os.path.isfile(path):
        paths = [path]
    else:
        raise Exception('Bad path')

    create_dish_desc = parsed_vars.pop('create_dish_desc')

    for path in paths:
        ingredients = {}
        season_links = {}
        recipes = []
        file_links = {}
        ingredients, season_links, recipes, file_links = chef.create_pierogi_desc(ingredients, season_links, recipes,
                                                                                  file_links, path)
        ingredients, season_links, recipes, file_links = create_dish_desc(ingredients, season_links, recipes,
                                                                          file_links, **parsed_vars)

        cooked_dish = chef.cook_dish_desc(ingredients, season_links, recipes, file_links)

        output_filename = output
        if output_filename is None:
            file_name = time.strftime("%Y%m%d-%H%M%S")

            output_filename = file_name + ".png"
            print("No output path provided, using " + output_filename)

        cooked_dish.save(output_filename)


if __name__ == "__main__":
    sys.exit(main())
