from .menu_item import MenuItem
from .threshold_order import ThresholdOrder
from ..dish_description import DishDescription, IngredientDesc


class SortOrder(MenuItem):
    @classmethod
    def add_desc(
            cls,
            dish_desc: DishDescription,
            path: str = None,
            target_pierogi_uuid=None,
            **kwargs
    ):
        """
        add the description of a sort from this path to the dish
        """
        if path is not None:
            target_pierogi_uuid = dish_desc.add_pierogi_desc(path)
            dish_desc.dish['pierogi'] = target_pierogi_uuid

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
        rotate_uuid = dish_desc.add_ingredient_desc(rotate_desc)

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
        sort_uuid = dish_desc.add_ingredient_desc(sort_desc)

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
        season_uuid = dish_desc.add_ingredient_desc(threshold_desc)
        dish_desc.add_seasoning_link(season_uuid, sort_uuid)

        dish_desc.extend_recipe([sort_uuid])

        return dish_desc

    @classmethod
    def add_parser_arguments(cls, parser):
        """
        add the arguments that a sort parser would need
        """
        parser.add_argument('-t', '--turns', default=0, type=int)
        parser.add_argument(
            '--ccw',
            dest='clockwise',
            action='store_false'
        )

        ThresholdOrder.add_parser_arguments(parser)
