"""
definition of ingredient base class
"""

import numpy as np
from PIL import Image


class Ingredient:
    """
    wrapper for a function to be applied to a grid of pixels.

    this base class defines some basic methods to be inherited and built upon,
    as well as a container for media represented as a numpy array.

    the two methods to be inherited and overridden are prep and cook.

    prep defines and sets the parameters of this image manipulation,
    and cook performs the maniuplation of the array.

    in this class, prep does nothing,
    and cook simply returns the instances static pixel array.
    """

    # used to fill in empty spots when cooked
    _black_pixel = np.array([0, 0, 0])
    _white_pixel = np.array([255, 255, 255])

    default_pixel = _black_pixel

    def __init__(self, opacity: int = 100, mask: np.ndarray = None, **kwargs):
        """
        :param pixels: if provided, these pixels will be returned by cook
        :param shape: if provided with no pixels, defines the (width, height)
        :param opacity: cook will overlay this % on input pixels
        :param mask: only cook with the pixels that are white in this mask
        :param kwargs: extra arguments to be passed to prep
        """
        self.opacity = opacity
        self.mask = mask
        self.prep(**kwargs)
        self.seasonings = []

    def prep(self, **kwargs):
        """
        parameterize the cook function
        """
        pass

    def cook(self, pixels: np.ndarray):
        """
        performs actions on a pixel array and returns a cooked array
        """
        return pixels

    def mask_pixels(self, pixels):
        masks = []

        for seasoning in self.seasonings:
            masks.append(seasoning.cook(pixels))

        mask = np.all(np.asarray(masks) == 255)

        return mask

    def season(self, seasoning):
        self.seasonings.append(seasoning)

    # def apply_mask(self, uncooked_pixels, cooked_pixels):
    #     """
    #     choose cooked over uncooked for white pixels in self.mask
    #
    #     :param uncooked_pixels: the pixels which will be covered
    #     :param cooked_pixels: the overlaying pixels
    #     """
    #     # use uncooked pixels as base
    #     masked_pixels = np.copy(uncooked_pixels)
    #
    #     # use the mask as guide for where to overlay
    #     mask = self.mask
    #     if mask is None:
    #         # all True
    #         binary_array = np.full(cooked_pixels.shape[:2], True)
    #     else:
    #         # True if white
    #         binary_array = np.all(mask == self._white_pixel, axis=2)
    #
    #     cooked_width = cooked_pixels.shape[0]
    #     cooked_height = cooked_pixels.shape[1]
    #     masked_pixels = np.resize(masked_pixels, (cooked_width, cooked_height, 3))
    #
    #     # layer cooked pixels over uncooked for true pixels (white in mask)
    #     masked_pixels[binary_array] = cooked_pixels[binary_array]
    #
    #     return masked_pixels
    #
    # def cook_mask(self, pixels: np.ndarray):
    #     """
    #     cook the pixels, then apply the ingredient's mask
    #     """
    #     cooked_pixels = self.cook(pixels)
    #     masked_pixels = self.apply_mask(pixels, cooked_pixels)
    #     return masked_pixels
