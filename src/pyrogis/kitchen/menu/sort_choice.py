from .menu_choice import MenuChoice
from .rotate_choice import RotateChoice
from .threshold_choice import ThresholdChoice
from ..ticket import Ticket, IngredientDesc
from ...ingredients import Sort


class SortChoice(MenuChoice):
    type_name = 'sort'
    type = Sort

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

        # create rotate description
        rotate_desc = IngredientDesc(
            type_name='rotate',
            kwargs={
                'turns': turns,
                'clockwise': clockwise,
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

    # put everything in cooked
    # if input dish was many, tell chef/kitchen to append a frame number
    #

    @classmethod
    def add_parser_arguments(cls, parser):
        """
        add the arguments that a sort parser would need
        """
        RotateChoice.add_parser_arguments(parser)

        ThresholdChoice.add_parser_arguments(parser)
