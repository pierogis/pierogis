from .menu_item import MenuItem
from .rotate_order import RotateOrder
from .threshold_order import ThresholdOrder
from ..ticket import Ticket, IngredientDesc
from ...ingredients import Pierogi, Sort


class SortOrder(MenuItem):
    type_name = 'sort'
    type = Sort

    @classmethod
    def generate_ticket(
            cls,
            ticket: Ticket,
            pierogi: Pierogi = None,
            target_pierogi_uuid=None,
            **kwargs
    ):
        """
        add the description of a sort from this path to the dish
        """
        if pierogi is not None:
            target_pierogi_uuid = ticket.add_pierogi(pierogi)
            ticket.base = target_pierogi_uuid

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

        # create the sort description
        sort_desc = IngredientDesc(
            type_name='sort',
            kwargs={
                'rotate': rotate_uuid,
                **kwargs
            }
        )
        sort_uuid = ticket.add_ingredient_desc(sort_desc)

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
        ticket.add_seasoning_link(season_uuid, sort_uuid)

        ticket.extend_recipe([sort_uuid])

        return ticket

    @classmethod
    def add_parser_arguments(cls, parser):
        """
        add the arguments that a sort parser would need
        """
        RotateOrder.add_parser_arguments(parser)

        ThresholdOrder.add_parser_arguments(parser)
