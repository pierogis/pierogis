from .menu_item import MenuItem
from .threshold_dish import ThresholdDish
from ..dish_description import DishDescription, IngredientDesc


class SortDish(MenuItem):
    @classmethod
    def add_desc(
            cls,
            dish_desc: DishDescription,
            path: str = None,
            **kwargs
    ):
        """
        add the description of a sort from this path to the dish
        """
        if path is not None:
            dish_desc = cls.add_pierogi_desc(dish_desc, path)

        # seasoning is for things that process but don't return a array
        sort_desc = IngredientDesc(
            type_name='sort',
            args=[],
            kwargs={
                **kwargs
            }
        )
        sort_uuid = dish_desc.add_ingredient_desc(sort_desc)

        # check for implied threshold
        lower_threshold = kwargs.pop('lower_threshold')
        upper_threshold = kwargs.pop('upper_threshold')
        if (lower_threshold is not None) or (upper_threshold is not None):
            threshold_desc = IngredientDesc(
                type_name='threshold',
                args=[],
                kwargs={
                    'lower_threshold': lower_threshold,
                    'upper_threshold': upper_threshold
                }
            )
            season_uuid = dish_desc.add_ingredient_desc(threshold_desc)
            dish_desc.add_seasoning(sort_uuid, season_uuid)

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

        ThresholdDish.add_parser_arguments(parser)
