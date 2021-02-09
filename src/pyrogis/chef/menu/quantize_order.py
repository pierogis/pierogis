from .menu_item import MenuItem

from ..dish_description import DishDescription, IngredientDesc
from ...ingredients import SpatialQuantize


class QuantizeOrder(MenuItem):
    @classmethod
    def add_desc(
            cls,
            dish_desc: DishDescription,
            path: str = None,
            **kwargs
    ):
        """
        add a description of a quantize recipe
        """
        if path is not None:
            target_pierogi_uuid = dish_desc.add_pierogi_desc(path)
            dish_desc.dish['pierogi'] = target_pierogi_uuid

        quantize_desc = IngredientDesc(
            type_name='quantize',
            kwargs=kwargs
        )

        quantize_uuid = dish_desc.add_ingredient_desc(quantize_desc)

        dish_desc.extend_recipe([quantize_uuid])

        return dish_desc

    @classmethod
    def add_parser_arguments(cls, parser):
        """
        add palette and palette size to this parser
        add rscolorq params to the parser and parent
        """

        # add palette and palette size
        parser.add_argument(
            '-c', '--colors',
            nargs='+',
            help='hex color codes to quantize to'
        )
        parser.add_argument(
            '-n', '--palette_size',
            type=int, default=SpatialQuantize.PALETTE_SIZE,
            help='number of colors in the palette'
        )

        parser.add_argument(
            '-i', '--iters',
            type=int, default=SpatialQuantize.ITERATIONS, dest='iterations',
            help='iterations per coarseness level'
        )
        parser.add_argument(
            '-r', '--repeats',
            type=int, default=SpatialQuantize.REPEATS,
            help='repeats per annealing temperature'
        )
        parser.add_argument(
            '--initial_temp',
            type=float, default=SpatialQuantize.INITIAL_TEMP,
            help='repeats per annealing temperature'
        )
        parser.add_argument(
            '--final_temp',
            type=float, default=SpatialQuantize.FINAL_TEMP,
            help='repeats per annealing temperature'
        )
        parser.add_argument(
            '-d', '--dithering_level',
            type=float, default=SpatialQuantize.DITHERING_LEVEL,
            help='repeats per annealing temperature'
        )
