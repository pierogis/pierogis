"""
threshold ingredient(s)
"""
import numpy as np

from .seasoning import Seasoning


class Threshold(Seasoning):
    """
    a seasoning that compares the brightness value of each pixel
    in the :param target pixel array and sets corresponding colors based on
    if it is "included" or not

    brightness = r * 0.299 + g * 0.587 + b * 0.114
    """

    LOWER_THRESHOLD = 60
    UPPER_THRESHOLD = 190

    lower_threshold: int
    upper_threshold: int
    inner: bool
    """if True, pixels between lower and upper are included"""

    def prep(
            self,
            lower_threshold: int = None,
            upper_threshold: int = None,
            inner: bool = False,
            **kwargs
    ):
        """
        set the threshold intensity levels

        calls Seasoning.prep with leftover kwargs

        pixels lower than lower_threshold
        or higher that upper_threshold
        are true (include_pixel)

        pixels with brightness >= upper_threshold
            or <= lower_threshold are replaced by include pixel (white)
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
        self.inner = inner

    def cook(self, pixels: np.ndarray):
        """
        parallel computation in rust is 10x speedup
        """
        input_pixels = pixels.copy()

        try:
            cooked_pixels = self.cook_rs(input_pixels)
        except:
            cooked_pixels = self.cook_np(input_pixels)

        return cooked_pixels

    def cook_np(self, pixels: np.ndarray):
        # perform the same operation as Threshold.cook, but only in numpy
        include_pixels = np.resize(self.include_pixel, pixels.shape)
        exclude_pixels = np.resize(self.exclude_pixel, pixels.shape)

        # use exclude_pixels as the base
        cooked_pixels = exclude_pixels
        # get intensities from average of rgb
        intensities_array = np.sum(
            pixels * np.asarray([0.299, 0.587, 0.114]), axis=2
        )
        if self.inner:
            # if intensity >= lower and <= upper, include
            boolean_array = np.logical_and(
                intensities_array <= self.upper_threshold,
                intensities_array >= self.lower_threshold
            )
        else:
            # if intensity <= lower or >= upper, include
            boolean_array = np.logical_or(
                intensities_array >= self.upper_threshold,
                intensities_array <= self.lower_threshold
            )

        # set True values in boolean_array to include_pixel
        cooked_pixels[boolean_array] = include_pixels[boolean_array]

        return cooked_pixels

    def cook_rs(self, pixels: np.ndarray):
        from pierogis_rs import algorithms

        include_pixel = self.include_pixel.astype(np.dtype('uint8'))
        exclude_pixel = self.exclude_pixel.astype(np.dtype('uint8'))

        # cook using the rust function
        cooked_pixels = algorithms.threshold(
            pixels.astype(np.dtype('uint8')),
            self.lower_threshold, self.upper_threshold,
            include_pixel,
            exclude_pixel,
            self.inner
        )

        return cooked_pixels
