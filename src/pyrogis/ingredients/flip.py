import numpy as np

from .ingredient import Ingredient


class Flip(Ingredient):
    """
    flip pixels about an axis
    """

    def prep(self, axis: int = 0):
        """
        :param axis: 0 to flip vertically, 1 to flip horizontally
        """

        self.axis = axis

    def cook(self, pixels: np.ndarray):
        """
        flip the pixels
        """
        flipped_pixels = np.flip(pixels, axis=self.axis)

        return flipped_pixels
