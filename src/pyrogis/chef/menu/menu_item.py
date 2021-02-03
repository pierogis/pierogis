import argparse
from abc import ABC, abstractmethod

from ..dish_description import DishDescription, IngredientDesc


class MenuItem(ABC):
    @classmethod
    @abstractmethod
    def add_desc(
            cls,
            dish_desc: DishDescription,
            path: str = None,
            **kwargs
    ):
        pass

    @staticmethod
    def add_pierogi_desc(dish_desc: DishDescription, path: str):
        """
        add a Pierogi IngredientDesc to and extend the recipe of dish_desc

        :param dish_desc: dish_desc to be extended
        :param path: path to be used to get the file of this Pierogi
        """
        file_uuid = dish_desc.add_file_link(path)

        ingredient_desc = IngredientDesc(
            type_name='pierogi',
            args=[],
            kwargs={
                'file': file_uuid
            }
        )

        # update the dish_desc
        pierogi_uuid = dish_desc.add_ingredient_desc(ingredient_desc)
        dish_desc.extend_recipe([pierogi_uuid])

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
