from abc import ABC
from abc import abstractmethod

import numpy as np
from PIL import Image

from .pixel import Pixel


class Ingredient(ABC):
    default_pixel = Pixel()

    def __init__(self, pixels: np.ndarray = None, width=0, height=0, opacity: int = 100, **kwargs):
        self.pixels = pixels
        self.width = width
        self.height = height
        self.opacity = opacity

        self.prep(**kwargs)

        if self.pixels is not None:
            self.width, self.height = self.pixels.shape[:2]
        else:
            self.pixels = np.full((self.height, self.width, 3), self.default_pixel)
            pass
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
    def cook(self, under_pixel: Pixel, x, y):
        pass

    # def season(self):
    #     pass
    #
    # def to_bytes(self):
    #     for ingredient in self.ingredients:
    #         self.layer(ingredient)
    #     self.input.show()
    #     ret = []
    #     for column in self.pixels:
    #         for pixel in column:
    #             ret.extend(pixel.tuple)
    #     return bytes(ret)

    @property
    def image(self):
        return Image.fromarray(self.pixels, 'RGB')

    def show(self):
        self.image.show()
