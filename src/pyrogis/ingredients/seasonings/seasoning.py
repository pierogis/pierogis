"""
seasoning base ingredient
"""

import numpy as np
from PIL import ImageColor

from pyrogis.ingredients.ingredient import Ingredient
from ..pierogi import Pierogi


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

    def prep(
            self,
            # pierogi: Pierogi,
            include: str = None,
            exclude: str = None,
            **kwargs
    ):
        """
        :param pierogi: If set, target will be the pixels that are cooked
        :param include: color to use for included pixels

        like little flakes of seasoning.

        can be hex

        :param exclude: color to use for excluded pixels
        """
        # self.pierogi = pierogi

        if include is None:
            include_pixel = self._white_pixel
        elif type(include) is str:
            if include[0] != '#':
                include = '#' + include
            include_pixel = ImageColor.getcolor(include, "RGB")
        else:
            include_pixel = include

        self.include_pixel = np.asarray(include_pixel)

        if exclude is None:
            exclude_pixel = self._black_pixel
        elif type(exclude) is str:
            if exclude[0] != '#':
                exclude = '#' + exclude
            exclude_pixel = ImageColor.getcolor(exclude, "RGB")
        else:
            exclude_pixel = exclude

        self.exclude_pixel = np.asarray(exclude_pixel)

    def cook(self, pixels: np.ndarray):
        """
        Pixels that match the include pixel should be set as the include pixel,
        otherwise set as the exclude pixel

        This isn't very useful, this is mostly an abstract class.
        """
        # turn pixels into boolean array
        # True replaces a pixel that matches self.include_pixel
        boolean_array = np.all(
            pixels == self.include_pixel, axis=2
        )

        # replace True with include_pixel and False with exclude_pixel
        binary_pixels = np.where(
            boolean_array, self.include_pixel, self.exclude_pixel
        )

        return binary_pixels

    # def season(self, recipient: Ingredient):
    #     """
    #     Set the input ingredient's mask to the output of a cook.
    #
    #     If self.target is none,
    #     recipient will be the pixels that are cooked as well.
    #
    #     :param recipient: ingredient which will have its mask set
    #     """
    #     recipient.mask = self.cook(self.pierogi.pixels)
    #
    #     return recipient
