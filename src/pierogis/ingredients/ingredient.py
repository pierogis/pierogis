# from abc import ABC
# from abc import abstractmethod

import numpy as np
from PIL import Image


class Ingredient:
    """Wrapper for a function to be applied to a grid of pixels.
    """

    # used to fill in empty spots when cooked
    _black_pixel = np.array([0, 0, 0])
    _white_pixel = np.array([255, 255, 255])

    default_pixel = _black_pixel

    def __init__(self, pixels: np.ndarray = None, origin: tuple = (0, 0), width: int = 0, height: int = 0,
                 opacity: int = 100, mask: np.ndarray = None, **kwargs):
        self.origin = origin
        self.opacity = opacity
        self.mask = mask

        if pixels is None:
            pixels = np.full((width, height, 3), self.default_pixel)

        self.pixels = pixels

        self.prep(**kwargs)

    @property
    def width(self):
        """From self.pixels
        """
        return self.pixels.shape[0]

    @property
    def height(self):
        """From self.pixels
        """
        return self.pixels.shape[1]

    # @property
    # def size(self):
    #     """(width, height)
    #     """
    #     return self.width, self.height

    @property
    def shape(self):
        """(width, height, 3)
        """
        return self.width, self.height, 3

    def prep(self, *args, **kwargs):
        """Parameterize the cook function
        """
        pass

    def get_image(self):
        image = Image.fromarray(np.rot90(self.pixels), 'RGB')
        return image

    def cook(self, pixels: np.ndarray):
        """Performs actions on a pixel array and returns a cooked array
        """
        return self.pixels

    def apply_mask(self, uncooked_pixels, cooked_pixels):
        masked_pixels = np.copy(uncooked_pixels)

        mask = self.mask
        if mask is None:
            binary_array = np.full(cooked_pixels.shape[:2], True)
        else:
            binary_array = np.all(mask == self._white_pixel, axis=2)
        masked_pixels[binary_array] = cooked_pixels[binary_array]

        return masked_pixels

    def cook_mask(self, pixels: np.ndarray):
        cooked_pixels = self.cook(pixels)
        masked_pixels = self.apply_mask(pixels, cooked_pixels)
        return masked_pixels

    def show(self):
        self.get_image().show()

    @staticmethod
    def mix_channel(under_val, over_val, opacity=100):
        return round((under_val * (100 - opacity) / 100) + (over_val * opacity / 100))
