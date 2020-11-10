"""pierogi.py
"""

import time
import io

from PIL import Image

from .ingredient import Ingredient
from .threshold import Threshold
from .pixel import Pixel

class Pierogi(Ingredient):
    """Image container for iterative pixel manipulation
    """

    def __init__(self, image: Image, **kwargs):
        super().__init__(size=image.size, **kwargs)
        self.image = image.convert('RGBA')

    def cook(self, pixel: Pixel, x: int, y: int):
        return Pixel(*self.image.load()[x, y])

    def show(self):
        self.image.show()