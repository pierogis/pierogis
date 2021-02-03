"""
define an image wrapper ingredient
"""

import numpy as np
from PIL import Image

from .ingredient import Ingredient


class Pierogi(Ingredient):
    """
    image container for iterative pixel manipulation

    uses PIL.Image to load to self.pixels
    """

    def prep(self, image: Image = None, file: str = None):
        """
        provide either a PIL Image or a path to an image file

        :param image: PIL Image that has already been loaded (takes precedence)
        :param file: file path to load from
        """
        if not image:
            image = Image.open(file)

        # rotate the image array on receipt so that
        # array dimensions are (width, height, 3)
        self.pixels = np.rot90(np.array(image.convert('RGB')), axes=(1, 0))

        # if self.height > 0 and self.width > 0:
        #     # truncate or fill pixels
        #     self.pixels = self.pixels.resize
        #     pass

    def cook(self, pixels: np.ndarray):
        """
        return a reshaped array of the image
        """

        return self.pixels.reshape(pixels.shape).astype(pixels.dtype)
