from .menu_item import MenuItem

from ...ingredients import SpatialQuantize


class QuantizeOrder(MenuItem):
    type_name = 'quantize'

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
            '--iterations',
            type=int, default=SpatialQuantize.ITERATIONS, dest='iterations',
            help='iterations per coarseness level'
        )
        parser.add_argument(
            '--repeats',
            type=int, default=SpatialQuantize.REPEATS,
            help='repeats per annealing temperature'
        )
        parser.add_argument(
            '--initial-temp',
            type=float, default=SpatialQuantize.INITIAL_TEMP,
            help='repeats per annealing temperature'
        )
        parser.add_argument(
            '--final-temp',
            type=float, default=SpatialQuantize.FINAL_TEMP,
            help='repeats per annealing temperature'
        )
        parser.add_argument(
            '--dithering-level',
            type=float, default=SpatialQuantize.DITHERING_LEVEL,
            help='repeats per annealing temperature'
        )
