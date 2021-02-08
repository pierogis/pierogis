import argparse
from abc import ABC, abstractmethod

from ..dish_description import DishDescription, PierogiDesc


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
