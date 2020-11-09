from abc import ABC
from abc import abstractmethod

from .pixel import Pixel

class Ingredient(ABC):
    default_pixel = Pixel(0,0,0,0)

    def __init__(self, pixel_array=None, opacity: int=100):
        self.width, self.height = pixel_array
        self.ingredients = []

        if pixel_array:
            self.pixel_array = pixel_array
            self.width, self.height = pixel_array
        else:
            self.pixel_array = [[self.default_pixel.place(x, y) for y in range(self.height)] for x in range(self.width)]
        
        self.opacity = opacity

    def add(self, ingredient: Ingredient):
        self.ingredients.append(ingredient)

    def mix(self, ingredient: Ingredient):
        under_pixel_array = self.pixel_array
        over_pixel_array = ingredient.pixel_array

        for y in range(len(under_pixel_array)):
            for x in range(len(y)):
                under_pixel = under_pixel_array[x][y]
                over_pixel = over_pixel_array[x][y]

                r = self.mix_channel(under_pixel.r, self.over_pixel.r)
                g = self.mix_channel(under_pixel.g, self.over_pixel.g)
                b = self.mix_channel(under_pixel.b, self.over_pixel.b)
                a = self.mix_channel(under_pixel.a, self.over_pixel.a)

        yield Ingredient()

    @staticmethod
    def mix_channel(under, over):
        return round((under * (100 - self.opacity) / 100)+ (over * self.opacity / 100))

    def season(self):
        pass
