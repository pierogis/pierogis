import argparse
from abc import ABC, abstractmethod

from ..ticket import Ticket, IngredientDesc
from ...ingredients import Pierogi


class MenuItem(ABC):
    type_name = None

    @classmethod
    def generate_ticket(
            cls,
            ticket: Ticket,
            pierogi: Pierogi = None,
            target_pierogi_uuid=None,
            **kwargs
    ):
        """
        add a description of a quantize recipe
        """
        if pierogi is not None:
            target_pierogi_uuid = ticket.add_pierogi(pierogi)
            ticket.base = target_pierogi_uuid

        ingredient_desc = IngredientDesc(
            type_name=cls.type_name,
            kwargs=kwargs
        )

        ingredient_uuid = ticket.add_ingredient_desc(ingredient_desc)

        ticket.extend_recipe([ingredient_uuid])

        return ticket

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
