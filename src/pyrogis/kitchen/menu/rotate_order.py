from pyrogis.kitchen.menu.menu_item import MenuItem
from pyrogis.ingredients import Rotate


class RotateOrder(MenuItem):
    type_name = 'rotate'
    type = Rotate

    @classmethod
    def add_parser_arguments(cls, parser):
        """
        add palette and palette size to this parser
        add rscolorq params to the parser and parent
        """

        # add palette and palette size
        parser.add_argument('-t', '--turns', default=0, type=int)
        parser.add_argument(
            '--ccw',
            dest='clockwise',
            action='store_false'
        )