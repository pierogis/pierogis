from abc import ABC
from abc import abstractmethod

import numpy as np

from .pixel import Pixel

class Ingredient(ABC):
    default_pixel = Pixel(0,0,0,0)

    def __init__(self, size=(0,0), pixels: np.ndarray=None, opacity: int=100):
        self.width, self.height = size

        if pixels:
            self.pixels = pixels
            self.width, self.height = pixels
        else:
            # self.pixel_array = [[self.default_pixel.place(x, y) for y in range(self.height)] for x in range(self.width)]

            self.pixels = np.full((self.width, self.height), self.default_pixel)

        self.opacity = opacity

    @property
    def size(self):
        """(width, height)
        """
        return (self.width, self.height)

    def cook(self, pixel: Pixel, x: int, y: int):
        under_pixel = pixel

        x, y = under_pixel.location
        over_pixel = self.pixels[x][y]

        cooked_pixel = under_pixel.mix(over_pixel, self.opacity)

        return cooked_pixel

    def season(self):
        pass
    
    def to_bytes(self):
        for ingredient in self.ingredients:
            self.layer(ingredient)
        self.input.show()
        ret = []
        for column in self.pixels:
            for pixel in column:
                ret.extend(pixel.tuple)
        return bytes(ret)