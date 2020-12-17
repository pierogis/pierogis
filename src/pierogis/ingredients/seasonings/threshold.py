import numpy as np

from pierogis.ingredients.seasonings.seasoning import Seasoning


class Threshold(Seasoning):
    """
    A seasoning that compares the average value (intesity) of each pixel in the :param target pixel array.
    When used in a mix, the threshold will target the pixel array below it if it has not been initialized with target.

    As it is a subclass of seasoning, a Threshold instance can use season method and work with or without a target
    """

    def prep(self, lower_threshold: int = 0, upper_threshold: int = 255, **kwargs):
        """
        Set the threshold intensity levels
        Pixels lower than :param lower_threshold or higher that :param upper_threshold are true (include_pixel)
        """
        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold

        # set include/exclude_pixel and target, if provided
        super().prep(**kwargs)

    def cook(self, pixels: np.ndarray):
        """
        Average values of rgb in :param pixels outside of intensity thresholds are true (include_pixel)
        """
        include_pixels = np.resize(self.include_pixel, pixels.shape)
        exclude_pixels = np.resize(self.exclude_pixel, pixels.shape)

        # use target, if available
        target_pixels = pixels
        if self.target is not None:
            target_pixels = self.target.pixels

        # use exclude_pixels as the base
        cooked_pixels = exclude_pixels
        # get intensities from average of rgb
        intensities_array = np.average(target_pixels, 2)
        # if intensity <= lower or >= upper, True
        boolean_array = np.logical_or(intensities_array >= self.upper_threshold,
                                      intensities_array <= self.lower_threshold)

        # set True values in boolean_array to include_pixel
        cooked_pixels[boolean_array] = include_pixels[boolean_array]

        return cooked_pixels
