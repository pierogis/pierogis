from typing import List

from .ingredient import Ingredient
from .pixel import Pixel


class Mix(Ingredient):

    def prep(self, **kwargs):
        ingredients = kwargs.get('ingredients')

        if ingredients is None:
            ingredients = []
        if isinstance(ingredients, list):
            self.ingredients = ingredients
        else:
            raise TypeError("kwarg 'ingredients' must be of type list")

    def cook(self, pixel: Pixel, x: int, y: int):
        under_pixel = pixel
        for ingredient in self.ingredients:
            cooked_pixel = ingredient.cook(under_pixel, x, y)

            mixed_pixel = Pixel.mix(under_pixel, cooked_pixel, self.opacity)

            under_pixel = mixed_pixel

        return mixed_pixel

    def add(self, ingredient: Ingredient):
        self.ingredients.append(ingredient)

    # def select(self):
    #     self.pixel_array

    #     return Ingredient()

    # def start(self):
    #     base = self.ingredients[0]
    #
    #     pixels = base.pixels
    #
    #     width, height = base.size
    #
    #     for x in range(width):
    #         for y in range(height):
    #             for pixel in self.cook(uncooked_pixel, x, y):
    #                 yield pixel
    #
    #             # for i in range(len(pixels)):
    #             #     pixels
