import argparse
from abc import ABC, abstractmethod

from ..ticket import Ticket, IngredientDesc


class MenuItem(ABC):
    type_name = None

    @classmethod
    def generate_ticket(
            cls,
            dish_desc: Ticket,
            path: str = None,
            target_pierogi_uuid=None,
            **kwargs
    ):
        """
        add a description of a quantize recipe
        """
        if path is not None:
            target_pierogi_uuid = dish_desc.add_pierogi(path)
            dish_desc.dish['pierogi'] = target_pierogi_uuid

        ingredient_desc = IngredientDesc(
            type_name=cls.type_name,
            kwargs=kwargs
        )

        quantize_uuid = dish_desc.add_ingredient_desc(ingredient_desc)

        dish_desc.extend_recipe([quantize_uuid])

        return dish_desc

    @classmethod
    def get_parser(cls):
        """
        get a parser for this menu item
        """
        parser = argparse.ArgumentParser(add_help=False)
        parser.set_defaults(generate_ticket=cls.generate_ticket)
        cls.add_parser_arguments(parser)

        return parser

    @classmethod
    @abstractmethod
    def add_parser_arguments(cls, parser):
        pass
