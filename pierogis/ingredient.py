from abc import ABC
from abc import abstractmethod

from .pixel import Pixel

class Ingredient(ABC):

    def __init__(self, size: tuple, opacity: int=100):
        self.width, self.height = size
        self.ingredients = []
        self.pixel_array = [[Pixel(0,0,0,0, x, y) for y in range(self.height)] for x in range(self.width)]
        self.opacity = opacity

    def __init__(self, opacity: int=100, mix_pixel:Pixel=Pixel() ):
        
        self.mix_pixel = mix_pixel

    def add(self, ingredient: Ingredient):
        self.ingredients.append(ingredient)

    def __mix(self, ingredient: Ingredient):
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

        return Ingredient(r, g, b, a, pixel.x, pixel.y)

    def cook(self):
        """Provide a pixel by pixel iterator of the manipulation
        """
        input_image = self.input

        # pixel = pixel_data[0, 0]

        # for ingredient in self.ingredients:
        #     if ingredient.blocking:
        #         ingredient(pierogi)

        for y in range(input_image.size[1]):
            for x in range(input_image.size[0]):
                # r, g, b = self.pixel_map[i, 0]
                threshold = Threshold(lower_threshold=100, upper_threshold=120)

                pixel = Pixel(*input_image.pixel_map[x, y], x, y)

                pierogi._pixel_array[x][y] = threshold.mix(pixel)

                yield Pierogi()

    @staticmethod
    def mix_channel(under, over):
        return round((under * (100 - self.opacity) / 100)+ (over * self.opacity / 100))