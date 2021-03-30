from .menu_choice import MenuChoice
from .custom_choice import CustomChoice
from .quantize_choice import QuantizeChoice
from .sort_choice import SortChoice
from .threshold_choice import ThresholdChoice
from .resize_choice import ResizeChoice
from .rotate_choice import RotateChoice

menu = {
    SortChoice.type_name: SortChoice,
    QuantizeChoice.type_name: QuantizeChoice,
    'custom': CustomChoice,
    ThresholdChoice.type_name: ThresholdChoice,
    ResizeChoice.type_name: ResizeChoice,
    'rotate': RotateChoice
}
