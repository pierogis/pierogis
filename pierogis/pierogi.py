"""pierogi.py
"""

import time
import io

from pandas import DataFrame
from PIL import Image

from .ingredient import Ingredient
from .threshold import Threshold
from .pixel import Pixel

class Pierogi(Ingredient):
    """High level pipeline for iterative pixel manipulation
    """

    def __init__(self, image: Image):
        super.__init__(image.size)
        self.input = image.convert('RGBA')
        self.input = image.convert('RGBA')
        self.pixel_map = self.image.load()
        # self.__grid = self.__load(image)
        self.ingredients = []
        self.width, self.height = self.image.size
        self._pixel_array = [[Pixel(0,0,0,0, x, y) for y in range(self.height)] for x in range(self.width)]

    # def __load(self, image: Image):
    #     # grid = DataFrame(index=range(self.width), columns=range(self.height))

    #     pixel_map = image.load()

    #     width, height = image.size

    #     start = time.perf_counter()

    #     i = 0

    #     for x in range(width):
    #         for y in range(height):
    #             i += 1
    #             cats = pixel_map[x,y]

    #     stop = time.perf_counter()

    #     print(stop - start)
        
    #     return grid

    def show(self):
        self.input.show()

    def layer(self, ingredient: Ingredient):
        opacity = 100
        for column in self._pixel_array:
            for pixel in column:
                original_pixel = self.input.pixel_map[pixel.x, pixel.y]
                r = self.mix_channel(pixel.r, self.mix_pixel.r)
                g = self.mix_channel(pixel.g, self.mix_pixel.g)
                b = self.mix_channel(pixel.b, self.mix_pixel.b)
                a = self.mix_channel(pixel.a, self.mix_pixel.a)

    def to_bytes(self):
        for ingredient in self.ingredients:
            self.layer(ingredient)
        self.input.show()
        ret = []
        for column in self._pixel_array:
            for pixel in column:
                ret.extend(pixel.tuple)
        return bytes(ret)