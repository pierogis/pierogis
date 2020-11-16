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

    def __init__(self, pixels: np.ndarray = None, origin: tuple = (0, 0), height: int = 0, width: int = 0,
                 opacity: int = 100, mask: np.ndarray = None):
        self.__pixels = pixels
        self.origin = origin
        self.opacity = opacity
        self.__height = height
        self.__width = width
        self.mask = mask

        if self.__pixels is not None:
            self.__height = self.pixels.shape[0]
            self.__width = self.pixels.shape[1]

    @property
    def pixels(self):
        pixels = self.__pixels
        if self.__pixels is None:
            pixels = np.full(self.shape, self.default_pixel)

        return pixels

    @property
    def width(self):
        """(width, height)
        """
        return self.__width

    @property
    def height(self):
        """(width, height)
        """
        return self.__height

    @property
    def size(self):
        """(width, height)
        """
        return self.height, self.width

    @property
    def shape(self):
        """(width, height)
        """
        return (*self.size, 3)

    def get_image(self):
        image = Image.fromarray(self.pixels, 'RGB')
        print(image.load()[0, 0])
        return image

    # @abstractmethod
    def prep(self):
        pass

    # @abstractmethod
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
            binary_array = np.all(mask == self._white_pixel)
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
