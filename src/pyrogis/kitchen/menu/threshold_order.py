from .menu_item import MenuItem

from ..ticket import Ticket, IngredientDesc
from ...ingredients import Threshold, Pierogi


class ThresholdOrder(MenuItem):
    type_name = 'threshold'
    type = Threshold

    @classmethod
    def generate_ticket(
            cls,
            dish_desc: Ticket,
            pierogi: Pierogi = None,
            target_pierogi_uuid=None,
            **kwargs
    ):
        """
        add a threshold recipe to the dish description
        """
        if pierogi is not None:
            target_pierogi_uuid = dish_desc.add_pierogi(pierogi)
            dish_desc.base = target_pierogi_uuid

        ingredient_desc = IngredientDesc(
            type_name='threshold',
            kwargs={
                'pierogi': target_pierogi_uuid,
                **kwargs
            }
        )

        # update the dish_desc
        threshold_uuid = dish_desc.add_ingredient_desc(ingredient_desc)
        dish_desc.extend_recipe([threshold_uuid])

        return dish_desc

    @classmethod
    def add_parser_arguments(cls, parser):
        """
        parse for thresholds
        """
        parser.add_argument(
            '-l', '--lower-threshold',
            default=Threshold.LOWER_THRESHOLD, type=int,
            help="Pixels with lightness below"
                 "this threshold are included"
        )
        parser.add_argument(
            '-u', '--upper-threshold',
            default=Threshold.UPPER_THRESHOLD, type=int,
            help="Pixels with lightness above"
                 "this threshold are included"
        )
        parser.add_argument(
            '-i', '--include',
            dest='include',
            default="ffffff", type=str,
            help="Hex color for included pixels"
        )
        parser.add_argument(
            '-e', '--exclude',
            dest='exclude',
            default="000000", type=str,
            help="Hex color for excluded pixels"
        )
