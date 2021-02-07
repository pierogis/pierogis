import os
from typing import List

import imageio as imageio
import numpy as np

from .ingredient import Ingredient
from .pierogi import Pierogi
from .recipe import Recipe


class Dish(Ingredient):
    """
    crop and cook an entire recipe for all pixels
    """

    @property
    def frames(self):
        return len(self.pierogis)

    def prep(self, recipe_generator, pierogis: List[Pierogi]=None, file=None, path=None):
        """
        set the recipe to cook for this dish
        """

        if pierogis is None:
            pierogis = []

            if file is not None:
                images = imageio.mimread(file)
                for image in images:
                    pierogis.append(Pierogi(pixels=np.asarray(image)))
            elif path is not None:
                pierogis = self.get_path_pierogis(path)

        self.pierogis = pierogis
        self.recipe_generator = recipe_generator

    @staticmethod
    def get_path_pierogis(path):
        pierogis = []

        for file in os.listdir(path):
            if not os.path.isfile(file):
                continue

            pierogis.append(Pierogi(file=file))

    def cook(self, pixels: np.ndarray):
        return self.recipe_generator(0, 0).cook(self.pierogis[0].pixels)

    def serve(self):
        """
        cook the recipe and set the output to this object's pixel array
        """
        cooked_pierogis = []

        for frame in range(self.frames):
            pierogi = self.pierogis[frame]
            # cook with these pixels as first input
            recipe = self.recipe_generator(frame + 1, self.frames)
            cooked_pixels = recipe.cook(pierogi.pixels)
            # ensure that the cooked pixels do not overflow 0-255
            clipped_pixels = np.clip(cooked_pixels, 0, 255)
            # # set the objects own pixels to the result of cooking
            cooked_pierogi = Pierogi(pixels=clipped_pixels)

            cooked_pierogis.append(cooked_pierogi)

        self.pierogis = cooked_pierogis

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