import numpy as np

from .ingredient import Ingredient

class Sort(Ingredient):

    def prep(self, **kwargs):
        ingredient = kwargs.get('ingredient')

    def cook(self, pixels: np.ndarray):
        intensities = np.average(pixels, axis=2)
        indices = np.argsort(intensities)

        sorted_pixels = pixels[np.arange(len(pixels))[:, np.newaxis], indices]

        return sorted_pixels