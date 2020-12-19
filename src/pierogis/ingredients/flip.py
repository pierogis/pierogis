import numpy as np

from .ingredient import Ingredient


class Flip(Ingredient):
    def prep(self, axis: int = 0):
        self.axis = axis

    def cook(self, pixels: np.ndarray):
        flipped_pixels = np.flip(pixels, axis=self.axis)

        return flipped_pixels