import numpy as np

from .seasoning import Seasoning

from .pixel import Pixel


class Threshold(Seasoning):
    lower_threshold: int = 0
    upper_threshold: int = 255
    inside: np.ndarray = np.array([0, 0, 0])
    outside: np.ndarray = np.array([255, 255, 255])

    def prep(self, lower_threshold: int = None, upper_threshold: int = None, inside: np.ndarray = None,
             outside: np.ndarray = None):
        if lower_threshold:
            self.lower_threshold = lower_threshold
        if upper_threshold:
            self.upper_threshold = upper_threshold
        if inside:
            self.inside = inside
        if outside:
            self.outside = outside

    def season(self):
        return self.cook(self.target.pixels)

    def cook(self, pixels: np.ndarray, mask: np.ndarray = None):
        inside_pixels = np.resize(self.inside, pixels.shape)
        outside_pixels = np.resize(self.outside, pixels.shape)

        cooked_pixels = inside_pixels
        masked_pixels = pixels[mask]
        intensities = np.average(pixels, 2)
        binary_pixels = np.logical_or(intensities >= self.upper_threshold, intensities <= self.lower_threshold)
        cooked_pixels[binary_pixels] = outside_pixels[binary_pixels]

        return cooked_pixels
