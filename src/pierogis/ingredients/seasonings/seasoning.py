"""Add a seasoning to an ingredient before you cook it
"""

import numpy as np

from pierogis.ingredients.ingredient import Ingredient


class Seasoning(Ingredient):
    """Seasonings can perform their computation before the cook stage.

    Seasonings are masks that use their season function to generate
    a selection of pixels to be operated on by a cook operation.

    They can be put into a mix to define a mask for a default
    target.pixels.shape sized "all passing" pixels.shape array.
    The can also be added to an ingredient through the season method.

    Return from cook should be binary (black_pixel, or white_pixel)
    """

    def __init__(self, target: Ingredient = None, **kwargs):
        super().__init__(**kwargs)

        self.target = target

    def prep(self, include_pixel: np.ndarray = None, exclude_pixel: np.ndarray = None):
        if include_pixel is None:
            include_pixel = self._white_pixel
        self.include_pixel = include_pixel

        if exclude_pixel is None:
            exclude_pixel = self._black_pixel
        self.exclude_pixel = exclude_pixel

    def season(self, ingredient: Ingredient):
        ingredient.mask = self.cook(self.target.pixels)

        return ingredient

    def cook(self, pixels: np.ndarray):
        # tries to use self.target and defaults to the passed in pixels
        target_pixels = self.get_target_pixels(pixels)

        boolean_array = np.all(target_pixels == self.include_pixel, axis=2)

        binary_pixels = np.where(boolean_array, self.exclude_pixel, self.include_pixel)
        return binary_pixels

    def get_target_pixels(self, pixels):
        target_pixels = pixels
        if self.target is not None:
            target_pixels = self.target.pixels


        return target_pixels