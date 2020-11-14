# from abc import ABC
# from abc import abstractmethod

import numpy as np
from PIL import Image

from .pixel import Pixel
from .seasoning import Seasoning


class Ingredient:
    """Wrapper for a function to be applied to a grid of pixels.
    """

    # used to fill in empty spots when cooked
    default_pixel = [0, 0, 0]

    def __init__(self, pixels: np.ndarray = None, height: int=0, width: int=0, opacity: int = 100, origin: tuple = (0, 0), **kwargs):
        self.pixels = pixels
        self.height = height
        self.width = width
        self.opacity = opacity
        self.origin = origin

        # prep is defined in subclasses as kwargs handlers
        self.prep(**kwargs)

        if self.pixels is not None:
            # if the subclass prep method set pixels already use those dimensions
            self.height, self.width = self.pixels.shape[:2]
        else:
            # else fill the dimensions provided with default_pixel
            self.pixels = np.full((self.height, self.width, 3), self.default_pixel)

    @property
    def size(self):
        """(width, height)
        """
        return self.width, self.height

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

    def season(self, seasoning: Seasoning):
        """Execute a seasoning object's season function
        Used to run a computation on a pixel array (within the seasoning) the cook phase
        """
        seasoning.season()

    def show(self):
        self.image.show()

    @staticmethod
    def mix_channel(under_val, over_val, opacity=100):
        return round((under_val * (100 - opacity) / 100) + (over_val * opacity / 100))