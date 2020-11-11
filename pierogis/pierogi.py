"""pierogi.py
"""

from PIL import Image
import numpy as np

from .ingredient import Ingredient
from .pixel import Pixel

from typing import TypeVar
from typing import Union


class Pierogi(Ingredient):
    """Image container for iterative pixel manipulation
    """

    def prep(self, **kwargs):
        image = kwargs.pop('image')
        if isinstance(image, str):
            image = Image.open(image)

        if isinstance(image, Image.Image):
            self.pixels = np.array(image.convert('RGB'))
        else:
            raise Exception("image should be str or PIL.Image")

    def cook(self, pixel: Pixel, x: int, y: int):
        return Pixel(*self.image.load()[x, y])
