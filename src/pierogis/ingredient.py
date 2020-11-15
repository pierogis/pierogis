# from abc import ABC
# from abc import abstractmethod

import numpy as np
from PIL import Image


class Ingredient:
    """Wrapper for a function to be applied to a grid of pixels.
    """

    # used to fill in empty spots when cooked
    default_pixel = [0, 0, 0]

    def __init__(self, pixels: np.ndarray = None, origin: tuple = (0, 0), height: int = 0, width: int = 0,
                 opacity: int = 100):
        self.pixels = pixels
        self.origin = origin
        self.opacity = opacity

        if self.pixels is None:
            # fill the dimensions provided with default_pixel
            self.pixels = np.full((height, width, 3), self.default_pixel)

    @property
    def width(self):
        """(width, height)
        """
        return self.pixels.shape[1]

    @property
    def height(self):
        """(width, height)
        """
        return self.pixels.shape[0]

    @property
    def size(self):
        """(width, height)
        """
        return self.pixels.shape[:2]

    @property
    def image(self):
        image = Image.fromarray(self.pixels, 'RGB')
        print(image.load()[0, 0])
        return image

    # @abstractmethod
    def prep(self, **kwargs):
        pass

    # @abstractmethod
    def cook(self, pixels: np.ndarray):
        """Performs actions on a pixel array and returns a cooked array
        """
        return self.pixels

    def show(self):
        self.image.show()

    @staticmethod
    def mix_channel(under_val, over_val, opacity=100):
        return round((under_val * (100 - opacity) / 100) + (over_val * opacity / 100))

    @staticmethod
    def mask(pixels, cooked_pixels, mask):
        if not mask:
            mask = np.full(pixels.size[:2], True)
        pixels[mask] = cooked_pixels[mask]

        return pixels
