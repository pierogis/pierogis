from .custom_filling import CustomFilling
from .filling import Filling
from .quantize_filling import QuantizeFilling
from .resize_filling import ResizeFilling
from .rotate_filling import RotateFilling
from .sort_filling import SortFilling
from .threshold_filling import ThresholdFilling
from .crop_filling import CropFilling
from .mmpx_filling import MMPXFilling

menu = {
    SortFilling.type_name: SortFilling,
    QuantizeFilling.type_name: QuantizeFilling,
    'custom': CustomFilling,
    ThresholdFilling.type_name: ThresholdFilling,
    ResizeFilling.type_name: ResizeFilling,
    RotateFilling.type_name: RotateFilling,
    CropFilling.type_name: CropFilling,
    MMPXFilling.type_name: MMPXFilling,
}
