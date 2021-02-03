from .custom_dish import CustomDish
from .quantize_dish import QuantizeDish
from .sort_dish import SortDish
from .threshold_dish import ThresholdDish

menu = {
    'sort': SortDish,
    'quantize': QuantizeDish,
    'chef': CustomDish,
    'threshold': ThresholdDish
}
