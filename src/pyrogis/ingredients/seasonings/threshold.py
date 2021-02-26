"""
threshold ingredient(s)
"""
import numpy as np
from pierogis_rs import algorithms

from .seasoning import Seasoning


class Threshold(Seasoning):
    """
    a seasoning that compares the brightness value of each pixel
    in the :param target pixel array.

    when used in a mix, the threshold will target the pixel array below it
    if it has not been initialized with target.

    as it is a subclass of seasoning,
    a Threshold instance has a season method to work with or without a target
    """

    LOWER_THRESHOLD = 100
    UPPER_THRESHOLD = 150

    lower_threshold: int
    """pixels below are `True`"""
    upper_threshold: int
    """pixels above are `True`"""

    def prep(
            self,
            lower_threshold: int = None,
            upper_threshold: int = None,
            **kwargs
    ):
        """
        set the threshold intensity levels

        calls Seasoning.prep with leftover kwargs

        pixels lower than lower_threshold
        or higher that upper_threshold
        are true (include_pixel)
        """
        # set include/exclude_pixel and target, if provided
        super().prep(**kwargs)

        if lower_threshold is None and upper_threshold is None:
            lower_threshold = self.LOWER_THRESHOLD
            upper_threshold = self.UPPER_THRESHOLD

        elif lower_threshold is None:
            lower_threshold = 0

        elif upper_threshold is None:
            upper_threshold = 255

        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold

    def cook(self, pixels: np.ndarray):
        """
        pixels with brightness >= upper_threshold
        or <= lower_threshold are replaced by include pixel (white)

        brightness = r * 0.299 + g * 0.587 + b * 0.114

        parallel computation in rust is 10x speedup
        """
        cooked_pixels = pixels.copy()

        # cook using the rust function
        cooked_pixels = algorithms.threshold(
            cooked_pixels.astype(np.dtype('uint8')),
            self.lower_threshold, self.upper_threshold,
            self.include_pixel.astype(np.dtype('uint8')),
            self.exclude_pixel.astype(np.dtype('uint8'))
        )

        return cooked_pixels

    def cook_np(self, pixels: np.ndarray):
        """
        perform the same operation as Threshold.cook, but only in numpy
        """

        include_pixels = np.resize(self.include_pixel, pixels.shape)
        exclude_pixels = np.resize(self.exclude_pixel, pixels.shape)

        # use exclude_pixels as the base
        cooked_pixels = exclude_pixels
        # get intensities from average of rgb
        intensities_array = np.sum(
            pixels * np.asarray([0.299, 0.587, 0.114]), axis=2
        )
        # if intensity <= lower or >= upper, True
        boolean_array = np.logical_or(
            intensities_array >= self.upper_threshold,
            intensities_array <= self.lower_threshold
        )

        # set True values in boolean_array to include_pixel
        cooked_pixels[boolean_array] = include_pixels[boolean_array]

        return cooked_pixels
