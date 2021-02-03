"""
seasoning ingredients

these ingredients apply their cook method
to create a mask for other ingredients to use
"""

from .seasoning import Seasoning
from .threshold import Threshold

__all__ = [
    'Seasoning',
    'Threshold'
]
