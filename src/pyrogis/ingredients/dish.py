from typing import List

import numpy as np

from .ingredient import Ingredient
from .pierogi import Pierogi
from .recipe import Recipe


class Dish(Ingredient):
    """
    crop and cook an entire recipe for all pixels
    """

    def prep(self, pierogis: List[Pierogi], recipe: Recipe):
        """
        set the recipe to cook for this dish

        :param base: base to start from
        :param recipe: recipe to cook and serve
        """

        self.pierogis = pierogis
        self.recipe = recipe

    def cook(self, pixels: np.ndarray):
        return self.serve().pixels

    def serve(self):
        """
        cook the recipe and set the output to this object's pixel array
        """
        cooked_pierogis = []

        for pierogi in self.pierogis:
            # cook with these pixels as first input
            cooked_pixels = self.recipe.cook(pierogi.pixels)
            # ensure that the cooked pixels do not overflow 0-255
            clipped_pixels = np.clip(cooked_pixels, 0, 255)
            # # set the objects own pixels to the result of cooking
            cooked_pierogi = Pierogi(pixels=clipped_pixels)

            cooked_pierogis.append(cooked_pierogi)

        animation = Animation(cooked_pierogis)

        return animation

    #
    # @property
    # def width(self):
    #     """
    #     width from self.pixels
    #     """
    #     return self.base.shape[0]
    #
    # @property
    # def height(self):
    #     """
    #     height from self.pixels
    #     """
    #     return self.recipe.base.shape[1]
    #
    # @property
    # def shape(self):
    #     """
    #     (width, height, 3)
    #     """
    #     return self.width, self.height, 3