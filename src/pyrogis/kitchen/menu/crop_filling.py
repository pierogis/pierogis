from typing import Tuple

from .filling import Filling
from ...ingredients import Crop


class CropFilling(Filling):
    type_name = 'crop'
    type = Crop

    @classmethod
    def add_parser_arguments(cls, parser):
        """parse for crop instructions"""
        parser.add_argument(
            '--height',
            type=int,
            help="height"
        )
        parser.add_argument(
            '--width',
            type=int,
            help="height"
        )
        parser.add_argument(
            '--aspect',
            type=int,
            help="height"
        )
        parser.add_argument(
            '-x',
            default=Crop.X,
            type=Tuple,
            help="height"
        )
        parser.add_argument(
            '-y',
            default=Crop.Y,
            type=int,
            help="height"
        )
