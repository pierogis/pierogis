import argparse
import os

from .menu_item import MenuItem
from ..dish_description import DishDescription


class CustomOrder(MenuItem):
    @staticmethod
    def read_recipe(dish_description: DishDescription, recipe_text: str, target_pierogi_uuid):
        """
        read a recipe from string to a DishDescription

        :param dish_description: the dish description to extend
        :param recipe_text: the recipe as a string like 'sort; quantize'
        """
        # split the recipe text by semi colons
        lines = recipe_text.split(';')

        # create the base parser for the recipe text
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()
        # add each parser described by the menu (quantize, sort, etc.)
        from . import menu
        for command, menu_item in menu.items():
            # add a parser from the given menu item's parser
            subparsers.add_parser(
                command,
                parents=[menu_item.get_parser()],
                add_help=False
            )

        # now parse each line
        for i in range(len(lines)):
            line = lines[i]
            # line may be just whitespace
            if not line.isspace():
                # split into different words
                phrases = line.strip().split()

                # use the parser with attached subparsers for the recipe names
                parsed, unknown = parser.parse_known_args(phrases)
                parsed_vars = vars(parsed)

                # this corresponds to one of the menu item's parser's
                # it links to a method on this class
                add_dish_desc = parsed_vars.pop('add_dish_desc')

                dish_description = add_dish_desc(
                    dish_description, target_pierogi_uuid=target_pierogi_uuid, **parsed_vars
                )

        return dish_description

    @classmethod
    def add_desc(
            cls,
            dish_desc: DishDescription,
            path=None,
            target_pierogi_uuid=None,
            **kwargs
    ):
        """
        add to dish_desc using a recipe specified in a string or a file
        """
        if path is not None:
            target_pierogi_uuid = dish_desc.add_pierogi_desc(path)
            dish_desc.dish['pierogi'] = target_pierogi_uuid

        # recipe can be provided as a string
        recipe = kwargs.pop('recipe')
        recipe_text = recipe

        # get recipe from file if this is a file
        if os.path.isfile(recipe):
            with open(recipe) as recipe_file:
                recipe_text = recipe_file.read()

        dish_desc = cls.read_recipe(dish_desc, recipe_text, target_pierogi_uuid)

        return dish_desc

    @classmethod
    def add_parser_arguments(cls, parser):
        parser.add_argument(
            'recipe',
            type=str, default='sort; quantize'
        )
