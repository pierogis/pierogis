"""Add a seasoning to an ingredient before you cook it
"""

import numpy as np

from pierogis.ingredients.ingredient import Ingredient


class Seasoning(Ingredient):
    """
    Seasonings can perform their computation before the cook stage.

    Seasonings are masks that use their season function to generate
    a selection of pixels to be operated on by a cook operation.

    They can be put into a mix to define a mask for a default
    target.pixels.shape sized "all passing" array.
    The can also be added to an ingredient through the season method.

    Return from cook should be binary (black_pixel, or white_pixel)
    """

    def prep(self, target: Ingredient = None, include_pixel: np.ndarray = None, exclude_pixel: np.ndarray = None, *args,
             **kwargs):
        self.target = target

        if include_pixel is None:
            include_pixel = self._white_pixel
        self.include_pixel = include_pixel

        if exclude_pixel is None:
            exclude_pixel = self._black_pixel
        self.exclude_pixel = exclude_pixel

    def season(self, ingredient: Ingredient):
        """
        Set the input ingredients mask to the output of cook
        Will cook :param ingredient or self.target, if present
        """

        target_pixels = ingredient.pixels
        if self.target is not None:
            target_pixels = self.target.pixels

        ingredient.mask = self.cook(target_pixels)

        return ingredient

    def cook(self, pixels: np.ndarray):
        # tries to use self.target and defaults to the passed in pixels
        target_pixels = pixels

        if self.target is not None:
            target_pixels = self.target.pixels

        # turn pixels into boolean array where True replaces a pixel that matches self.include_pixel
        boolean_array = np.all(target_pixels == self.include_pixel, axis=2)

        # replace True with include_pixel and False with exclude_pixel
        binary_pixels = np.where(boolean_array, self.include_pixel, self.exclude_pixel)
        return binary_pixels
