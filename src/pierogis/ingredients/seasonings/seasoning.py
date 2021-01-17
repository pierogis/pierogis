"""Add seasoning to an ingredient before you cook it
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
        """
        :param target: If set, target will be the pixels that are cooked
        :param include_pixel: The color to be used if a cooking pixel is to be included.
        Think of them like little flakes of seasoning
        :param exclude_pixel: The color to be used if a cooking pixel is not to be included
        """
        self.target = target

        if include_pixel is None:
            include_pixel = self._white_pixel
        self.include_pixel = include_pixel

        if exclude_pixel is None:
            exclude_pixel = self._black_pixel
        self.exclude_pixel = exclude_pixel

    def season(self, recipient: Ingredient):
        """
        Set the input ingredient's mask to the output of a cook.
        If self.target is none, recipient will be the pixels that are cooked as well.

        :param recipient: ingredient which will have its mask set
        """

        recipient_pixels = recipient.pixels

        recipient.mask = self.cook(recipient_pixels)

        return recipient

    def cook(self, pixels: np.ndarray):
        """
        Pixels that match the include pixel should be set as the include pixel, otherwise set as the exclude pixel
        This isn't very useful, this is mostly an abstract class.
        """
        # tries to use self.target and defaults to the passed in pixels
        target_pixels = pixels

        if self.target is not None:
            target_pixels = self.target.pixels

        # turn pixels into boolean array where True replaces a pixel that matches self.include_pixel
        boolean_array = np.all(target_pixels == self.include_pixel, axis=2)

        # replace True with include_pixel and False with exclude_pixel
        binary_pixels = np.where(boolean_array, self.include_pixel, self.exclude_pixel)
        return binary_pixels
