from abc import ABC
from abc import abstractmethod

import numpy as np
from PIL import Image

from .pixel import Pixel


class Ingredient(ABC):
    default_pixel = [0, 0, 0]

    def __init__(self, pixels: np.ndarray = None, height=0, width=0, opacity: int = 100, **kwargs):
        self.pixels = pixels
        self.height = height
        self.width = width
        self.opacity = opacity

        self.prep(**kwargs)

        if self.pixels is not None:
            self.height, self.width = self.pixels.shape[:2]
        else:
            self.pixels = np.full((self.height, self.width, 3), self.default_pixel)
            # self.pixels = np.full((1, 1), self.default_pixel)

    @property
    def size(self):
        """(width, height)
        """
        return self.width, self.height

    @abstractmethod
    def prep(self, **kwargs):
        pass

    @abstractmethod
    def cook(self, pixels: np.ndarray):
        pass

    @property
    def image(self):
        image = Image.fromarray(self.pixels, 'RGB')
        print(image.load()[0, 0])
        return image

    def show(self):
        self.image.show()

    @staticmethod
    def mix_channel(under_val, over_val, opacity=100):
        return round((under_val * (100 - opacity) / 100) + (over_val * opacity / 100))