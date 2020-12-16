import numpy as np

from pierogis.ingredients.ingredient import Ingredient
from pierogis.ingredients.mix import Mix


class Dish(Ingredient):
    """Crop and cook an entire recipe for all pixels
    """

    def prep(self, mix: Mix):
        self.mix = mix

    def cook(self, pixels: np.ndarray):
        return self.mix.cook_mask(pixels)

    def serve(self):
        pixels = self.pixels
        if self.size == (0, 0):
            base = self.mix.ingredients[0]
            width, height = base.size

            pixels = np.full((height, width, 3), self.default_pixel)

        cooked_pixels = self.cook(pixels.astype('uint32'))

        clipped_pixels = np.clip(cooked_pixels, 0, 255)

        self.pixels = clipped_pixels.astype('uint8')
