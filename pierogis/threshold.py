import numpy as np

from .ingredient import Ingredient

from .pixel import Pixel


class Threshold(Ingredient):
    def prep(self, **kwargs):
        self.lower_threshold = kwargs.get('lower_threshold', 0)
        self.upper_threshold = kwargs.pop('upper_threshold', 128)
        self.inside = kwargs.pop('inside', [0, 0, 0])
        self.outside = kwargs.pop('outside', [255, 255, 255])

    # def cook(self, r, g, b, x: int, y: int):
    #
    #     if sum(r, g, b) / 3 > self.upper_threshold:
    #         cooked_pixel = [255, 255, 255]
    #
    #     else:
    #         cooked_pixel = [0, 0, 0]
    #
    #     return cooked_pixel

    def cook(self, pixels: np.ndarray):
        cooked_pixels = np.full(pixels.shape, self.inside)
        binary_pixels = np.logical_or(np.average(pixels, 2) >= self.upper_threshold, np.average(pixels, 2) <= self.lower_threshold)
        cooked_pixels[binary_pixels] = self.outside

        return cooked_pixels
    # def cook(self, pixel: Pixel, x: int, y: int):
    #     if pixel.intensity > self.upper_threshold:
    #         cooked_pixel = Pixel(255, 255, 255)
    #
    #     else:
    #         cooked_pixel = Pixel(0, 0, 0)
    #
    #     return cooked_pixel
