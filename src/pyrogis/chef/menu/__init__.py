from .custom_order import CustomOrder
from .quantize_order import QuantizeOrder
from .sort_order import SortOrder
from .threshold_order import ThresholdOrder

menu = {
    'sort': SortOrder,
    'quantize': QuantizeOrder,
    'chef': CustomOrder,
    'threshold': ThresholdOrder
}
