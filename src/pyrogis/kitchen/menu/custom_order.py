import argparse
import os

from .menu_item import MenuItem
from ..ticket import Ticket
from ...ingredients import Pierogi


class CustomOrder(MenuItem):
    @staticmethod
    def read_recipe(
            ticket: Ticket,
            recipe_text: str,
            target_pierogi_uuid
    ):
        """
        read a recipe from string, adding to a DishDescription

        :param ticket: the dish description to extend
        :param recipe_text: the recipe as a string like 'sort; quantize'
        :param target_pierogi_uuid: the uuid of the base pierogi for the dish
        """
        # split the recipe text by semi colons
        recipe_items = recipe_text.split(';')

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
        for order in recipe_items:
            # line may be just whitespace
            if order.isspace() or order == '':
                continue
            else:
                # split into different words
                phrases = order.strip().split()

                # use the parser with attached subparsers for the recipe names
                parsed, unknown = parser.parse_known_args(phrases)
                parsed_vars = vars(parsed)

                # this corresponds to one of the menu item's parser's
                # it links to a method on this class
                extend_ticket = parsed_vars.pop('extend_ticket')

                ticket = extend_ticket(
                    ticket, target_pierogi_uuid=target_pierogi_uuid, **parsed_vars
                )

        return ticket

    @classmethod
    def generate_ticket(
            cls,
            ticket: Ticket,
            pierogi: Pierogi = None,
            target_pierogi_uuid=None,
            **kwargs
    ):
        """
        add to dish_desc using a recipe specified in a string or a file
        """
        if pierogi is not None:
            target_pierogi_uuid = ticket.add_pierogi(pierogi)
            ticket.base = target_pierogi_uuid

        # recipe can be provided as a string
        recipe = kwargs.pop('recipe')
        recipe_text = recipe

        # get recipe from file if this is a file
        if os.path.isfile(recipe):
            with open(recipe) as recipe_file:
                recipe_text = recipe_file.read()

        ticket = cls.read_recipe(ticket, recipe_text, target_pierogi_uuid)

        return ticket

    @classmethod
    def add_parser_arguments(cls, parser):
        parser.add_argument(
            'recipe',
            type=str, default='sort; quantize'
        )
