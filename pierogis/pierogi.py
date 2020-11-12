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
        image = kwargs.get('image')
        if not image:
            file = kwargs.get('file')
            image = Image.open(file)

        self.pixels = np.array(image.convert('RGB'))

    # def cook(self, pixel: Pixel, x: int, y: int):
    #     return Pixel(*self.image.load()[x, y])

    def cook(self, pixels: np.ndarray):
        """Return a cropped array of the image
        """

        pixels = self.pixels.reshape(pixels.shape)
        return pixels
