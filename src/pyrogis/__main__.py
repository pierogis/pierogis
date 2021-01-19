import argparse
import os
import sys
import time

from .chef import Chef, DishDescription

chef = Chef()


def parse_args(args: list):
    """
    use a chef to parse args into specified command
    """
    # create top level parser
    parser = argparse.ArgumentParser(description='** image processing pipelines **')
    subparsers = parser.add_subparsers(dest='recipe', required=True)

    # create parent parser to pass down arguments only
    parent_parser = argparse.ArgumentParser()
    parent_parser.add_argument('path', default='./', help='path to file or directory to use as input')
    parent_parser.add_argument('-o', '--output', help='path and filename to save resulting image')

    for command, command_parser in chef.menu.items():
        # inherit the parent class arguments and the arguments specific to a subcommand
        subparsers.add_parser(command, parents=[parent_parser, command_parser], add_help=False)

    # parse the input args with the applicable arguments attached
    parsed = parser.parse_args(args)
    parsed_vars = vars(parsed)
    # need the path to use as input for some recipes like opening files for ingredients
    path = parsed_vars.pop('path')
    # need to take out output because it is just used for cli stuff
    output = parsed_vars.pop('output')

    # this is a default parameter attached to subparsers that is a function for handling its options
    add_dish_desc = parsed_vars.pop('add_dish_desc')

    return path, output, parsed_vars, add_dish_desc


def create_dish(path: str, add_dish_desc, parsed_vars):
    """
    create and cook the specified dish with the vars

    :param path: path to use for the media in the dish
    :param add_dish_desc: chef method used to handle the parsed_vars
    :param parsed_vars: arguments to the recipe to create
    """
    dish_desc = DishDescription()
    # use the parser attached function to create a dish description for the specified cli recipe
    dish_desc = add_dish_desc(dish_desc, path=path, **parsed_vars)

    # cook the generated description
    return chef.cook_dish_desc(dish_desc)


def main(args=None):
    """cli program"""
    if args is None:
        args = sys.argv[1:]

    path, output, parsed_vars, add_dish_desc = parse_args(args)

    # check if the path given contains many media
    if os.path.isdir(path):
        paths = [path + '/' + filename for filename in os.listdir(path)]
    elif os.path.isfile(path):
        paths = [path]
    else:
        raise Exception('Bad path')

    # loop through the potential media paths
    for path in paths:
        cooked_dish = create_dish(path, add_dish_desc, parsed_vars)

        # use the output popped from arguments to make a filename
        output_filename = output
        if output_filename is None:
            file_name = time.strftime("%Y%m%d-%H%M%S")

            output_filename = file_name + ".png"
            print("No output path provided, using " + output_filename)

        # save to the outcome filename
        cooked_dish.save(output_filename)


if __name__ == "__main__":
    sys.exit(main())
