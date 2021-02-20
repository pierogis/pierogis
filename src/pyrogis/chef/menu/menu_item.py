import argparse
from abc import ABC, abstractmethod

from ..dish_description import DishDescription, PierogiDesc, IngredientDesc


class MenuItem(ABC):
    type_name = None

    @classmethod
    @abstractmethod
    def add_desc(
            cls,
            dish_desc: DishDescription,
            path: str = None,
            target_pierogi_uuid=None,
            **kwargs
    ):
        """
        add a description of a quantize recipe
        """
        if path is not None:
            target_pierogi_uuid = dish_desc.add_pierogi_desc(path)
            dish_desc.dish['pierogi'] = target_pierogi_uuid

        resize_desc = IngredientDesc(
            type_name=cls.type_name,
            kwargs=kwargs
        )

        quantize_uuid = dish_desc.add_ingredient_desc(resize_desc)

        dish_desc.extend_recipe([quantize_uuid])

        return dish_desc

    @classmethod
    def get_parser(cls):
        """
        get a parser for this menu item
        """
        parser = argparse.ArgumentParser(add_help=False)
        parser.set_defaults(add_dish_desc=cls.add_desc)
        cls.add_parser_arguments(parser)

        return parser

    @classmethod
    @abstractmethod
    def add_parser_arguments(cls, parser):
        pass
