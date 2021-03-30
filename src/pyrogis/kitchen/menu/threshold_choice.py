from .menu_choice import MenuChoice
from ...ingredients import Threshold


class ThresholdChoice(MenuChoice):
    type_name = 'threshold'
    type = Threshold

    @classmethod
    def add_parser_arguments(cls, parser):
        """
        parse for thresholds
        """
        parser.add_argument(
            '-l', '--lower-threshold',
            default=Threshold.LOWER_THRESHOLD, type=int,
            help="Pixels with lightness below"
                 "this threshold are included"
        )
        parser.add_argument(
            '-u', '--upper-threshold',
            default=Threshold.UPPER_THRESHOLD, type=int,
            help="Pixels with lightness above"
                 "this threshold are included"
        )
        parser.add_argument(
            '-i', '--include',
            dest='include',
            default="ffffff", type=str,
            help="Hex color for included pixels"
        )
        parser.add_argument(
            '-e', '--exclude',
            dest='exclude',
            default="000000", type=str,
            help="Hex color for excluded pixels"
        )
