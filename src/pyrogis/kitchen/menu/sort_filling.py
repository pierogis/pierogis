import argparse

from .filling import Filling
from .rotate_filling import RotateFilling
from .threshold_filling import ThresholdFilling
from ..ticket import Ticket, IngredientDesc
from ...ingredients import Sort, Ingredient


class SortFilling(Filling):
    type_name: str = 'sort'
    type: Ingredient = Sort

    @classmethod
    def add_parser_arguments(cls, parser: argparse.ArgumentParser):
        """
        add the arguments that a sort parser would need
        """
        RotateFilling.add_parser_arguments(parser)

        ThresholdFilling.add_parser_arguments(parser)

        parser.set_defaults(angle=0)

    @classmethod
    def generate_ticket(
            cls,
            ticket: Ticket,
            path: str = None,
            frame_index: int = 0,
            target_pierogi_uuid: str = None,
            **kwargs
    ):
        """
        add the description of a sort from this path to the dish
        """

        turns = kwargs.pop('turns')
        clockwise = kwargs.pop('clockwise')
        angle = kwargs.pop('angle')
        resample = kwargs.pop('resample')

        # create rotate description
        rotate_desc = IngredientDesc(
            type_name='rotate',
            kwargs={
                'turns': turns,
                'angle': angle,
                'clockwise': clockwise,
                'resample': resample
            }
        )
        rotate_uuid = ticket.add_ingredient_desc(rotate_desc)

        # check for implied threshold
        lower_threshold = kwargs.pop('lower_threshold')
        upper_threshold = kwargs.pop('upper_threshold')

        # create threshold desc
        threshold_desc = IngredientDesc(
            type_name='threshold',
            kwargs={
                'lower_threshold': lower_threshold,
                'upper_threshold': upper_threshold,
                'pierogi': target_pierogi_uuid
            }
        )
        # add seasoning link for threshold to season sort
        season_uuid = ticket.add_ingredient_desc(threshold_desc)

        kwargs['rotate'] = rotate_uuid

        ticket = super().generate_ticket(
            ticket, path, frame_index, target_pierogi_uuid, **kwargs
        )

        sort_uuid = ticket.recipe[-1]

        ticket.add_seasoning_link(season_uuid, sort_uuid)

        return ticket
