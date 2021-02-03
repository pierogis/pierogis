from .menu_item import MenuItem

from ..dish_description import DishDescription, IngredientDesc
from ...ingredients import Threshold


class ThresholdDish(MenuItem):
    @classmethod
    def add_desc(
            cls,
            dish_desc: DishDescription,
            path: str = None,
            **kwargs
    ):
        """
        add a threshold recipe to the dish description
        """
        if path is not None:
            dish_desc = cls.add_pierogi_desc(dish_desc, path)

        ingredient_desc = IngredientDesc(
            type_name='threshold',
            args=[],
            kwargs={
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
                 "this threshold will not get sorted"
        )
        parser.add_argument(
            '-u', '--upper-threshold',
            default=Threshold.UPPER_THRESHOLD, type=int,
            help="Pixels with lightness above"
                 "this threshold will not get sorted"
        )
