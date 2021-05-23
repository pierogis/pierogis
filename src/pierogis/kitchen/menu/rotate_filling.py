from .filling import Filling
from ...ingredients import Rotate


class RotateFilling(Filling):
    type_name = 'rotate'
    type = Rotate

    @classmethod
    def add_parser_arguments(cls, parser):
        """
        add palette and palette size to this parser
        add rscolorq params to the parser and parent
        """

        # add palette and palette size
        parser.add_argument('-t', '--turns', default=1, type=int)
        parser.add_argument('-a', '--angle', default=90, type=int)
        parser.add_argument(
            '--ccw',
            dest='clockwise',
            action='store_false'
        )
        parser.add_argument(
            '--resample-filter',
            dest='resample',
            default=Rotate.DEFAULT_RESAMPLE,
            choices=Rotate.FILTERS.keys(),
            help='resample filter for resize'
        )
