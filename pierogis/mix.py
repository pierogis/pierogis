from typing import List

from .ingredient import Ingredient
from .pixel import Pixel

class Mix(Ingredient):

    def __init__(self, ingredients: List[Ingredient]=None, **kwargs):
        super().__init__(**kwargs)
        if ingredients is None:
            ingredients = []
        self.ingredients = ingredients

    def add(self, ingredient: Ingredient):
        self.ingredients.append(ingredient)

    def cook(self, pixel: Pixel, x: int, y: int):
        cooked_pixel = pixel
        for ingredient in self.ingredients:
            yield ingredient.cook(cooked_pixel, x, y)

    # def select(self):
    #     self.pixel_array

    #     return Ingredient()

    def start(self):
        base = self.ingredients[0]

        pixels = base.pixels

        width, height = base.size

        for x in range(width):
            for y in range(height):
                for pixel in self.cook(uncooked_pixel, x, y):
                    yield pixel

                # for i in range(len(pixels)):
                #     pixels