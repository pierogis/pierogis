import numpy as np

from pierogis.ingredients.seasonings.seasoning import Seasoning


class Threshold(Seasoning):

    def prep(self, lower_threshold: int = 0, upper_threshold: int = 255, **kwargs):
        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold

        super().prep(**kwargs)

    def cook(self, pixels: np.ndarray):
        include_pixels = np.resize(self.include_pixel, pixels.shape)
        exclude_pixels = np.resize(self.exclude_pixel, pixels.shape)

        target_pixels = self.get_target_pixels(pixels)

        cooked_pixels = exclude_pixels
        intensities_array = np.average(target_pixels, 2)
        boolean_array = np.logical_or(intensities_array >= self.upper_threshold, intensities_array <= self.lower_threshold)
        cooked_pixels[boolean_array] = include_pixels[boolean_array]

        return cooked_pixels
