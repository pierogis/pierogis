import numpy as np

from .ingredient import Ingredient
from .mix import Mix
from .pixel import Pixel

class Dish(Ingredient):
    """Crop and cook an entire recipe for all pixels
    """

    def prep(self, **kwargs):
        self.mix = kwargs.pop('mix')

    def cook(self, pixels: np.ndarray):
        return self.mix.cook(pixels)

    # def serve(self):
    #     if self.size == (0, 0):
    #         base = self.mix.ingredients[0]
    #         self.width, self.height = base.size
    #
    #         self.pixels = np.full((self.width, self.height), self.default_pixel)
    #
    #     for x in range(self.width):
    #         for y in range(self.height):
    #             self.pixels[y][x] = self.mix.cook(*self.pixels[y][x], x, y)

    def serve(self):
        pixels = self.pixels
        if self.size == (0, 0):
            base = self.mix.ingredients[0]
            width, height = base.size

            pixels = np.full((width, height), self.default_pixel)

        cooked_pixels = self.cook(pixels.astype('uint32'))

        clipped_pixels = np.clip(cooked_pixels, 0, 255)

        self.pixels = clipped_pixels.astype('uint8')

    # taste test - serve and cook each ingredient simulatneously