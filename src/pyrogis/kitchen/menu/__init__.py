from .filling import Filling
from .custom_filling import CustomFilling
from .quantize_filling import QuantizeFilling
from .sort_filling import SortFilling
from .threshold_filling import ThresholdFilling
from .resize_filling import ResizeFilling
from .rotate_filling import RotateFilling

menu = {
    SortFilling.type_name: SortFilling,
    QuantizeFilling.type_name: QuantizeFilling,
    'custom': CustomFilling,
    ThresholdFilling.type_name: ThresholdFilling,
    ResizeFilling.type_name: ResizeFilling,
    'rotate': RotateFilling
}
