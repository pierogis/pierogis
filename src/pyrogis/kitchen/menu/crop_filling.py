from .filling import Filling
from ...ingredients import Crop
from ...ingredients.seasonings.rectangle import Direction, Rectangle


class CropFilling(Filling):
    type_name = 'crop'
    type = Crop

    @classmethod
    def add_parser_arguments(cls, parser):
        """parse for crop instructions"""
        parser.add_argument(
            '--origin',
            default=Rectangle.ORIGIN,
            type=Direction,
            choices=list(Direction),
            help="origin location; sw -> (0,0); ne -> (input width,input height)... etc"
        )
        parser.add_argument(
            '--height',
            type=int,
            help="height of crop selection"
        )
        parser.add_argument(
            '--width',
            type=int,
            help="width of crop selection"
        )
        parser.add_argument(
            '--aspect',
            type=float,
            help="aspect ratio; ignored if height and width provided"
        )

        def int_or_float(value: str):
            f = float(value)
            if f.is_integer():
                return int(f)
            else:
                return f

        parser.add_argument(
            '-x',
            default=Crop.X,
            type=int_or_float,
            help="x offset from the origin; can be negative;"
                 "if a float, corresponds to that percentage of the input image width"
        )
        parser.add_argument(
            '-y',
            default=Crop.Y,
            type=int_or_float,
            help="y offset from the origin; can be negative;"
                 "if a float, corresponds to that percentage of the input image height"
        )
