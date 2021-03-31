"""
definition of ingredient base class
"""

import numpy as np


class Ingredient:
    """
    wrapper for a function to be applied to a grid of pixels.

    this base class defines some basic methods to be inherited and built upon,
    as well as a container for media represented as a numpy array.

    the two methods to be inherited and overridden are prep and cook.

    prep defines and sets the parameters of this image manipulation,
    and cook performs the manipulation of the array.

    in this base class, cook and prep do nothing
    """

    # used to fill in empty spots when cooked
    _black_pixel = np.array([0, 0, 0])
    _white_pixel = np.array([255, 255, 255])

    _default_pixel = _white_pixel

    def __init__(self, opacity: int = 100, mask: np.ndarray = None, **kwargs):
        """
        :param opacity: cook will overlay this % on input pixels

        :param mask: only cook with the pixels that are white in this mask

        :param kwargs: extra arguments to be passed to prep
        """
        self.opacity = opacity
        """opacity when overlaying on previous output"""
        self.mask = mask
        """opacity when overlaying"""
        self.prep(**kwargs)
        self.seasonings = []

    def prep(self, **kwargs) -> None:
        """
        parameterize the cook function
        """
        pass

    def cook(self, pixels: np.ndarray) -> np.ndarray:
        """
        performs actions on a pixel array and returns a cooked array
        """
        return pixels

    def mask_pixels(self, pixels):
        """
        create a black and white mask from pixels
        and the seasonings attached to this ingredient

        :param pixels: pixels to create a mask from
        """
        white_pixels = np.resize(self._white_pixel, pixels.shape)

        base_mask = self.mask
        if base_mask is None:
            base_mask = white_pixels

        masks = [base_mask]

        for seasoning in self.seasonings:
            masks.append(seasoning.cook(pixels))

        binary_array = np.all(np.asarray(masks) == 255, axis=0)

        black_pixels = np.resize(self._black_pixel, pixels.shape)

        mask = black_pixels

        mask[binary_array] = white_pixels[binary_array]

        return mask

    def season(self, seasoning: 'Ingredient'):
        """
        add an ingredient whose cook function is
        used to produce this ingredients mask
        """
        self.seasonings.append(seasoning)
