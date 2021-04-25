from .filling import Filling
from ...ingredients import Threshold


class ThresholdFilling(Filling):
    type_name = 'threshold'
    type = Threshold

    @classmethod
    def add_parser_arguments(cls, parser):
        """
        parse for thresholds
        """
        parser.add_argument(
            '-l', '--lower-threshold',
            type=float,
            help="lower end threshold value"
        )
        parser.add_argument(
            '-u', '--upper-threshold',
            type=float,
            help="upper end threshold value"
        )
        parser.add_argument(
            '--inner',
            dest='inner',
            action='store_true',
            help="provide to include pixels between the threshold values"
        )
        parser.add_argument(
            '--include',
            dest='include',
            default="ffffff", type=str,
            help="Hex color for included pixels"
        )
        parser.add_argument(
            '--exclude',
            dest='exclude',
            default="000000", type=str,
            help="Hex color for excluded pixels"
        )
