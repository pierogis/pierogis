import numpy as np

from pierogis.ingredients.ingredient import Ingredient

class Sort(Ingredient):

    def prep(self, **kwargs):
        self.target = kwargs.get('target')
        self.delimiter = kwargs.get('delimiter', np.array([255, 255, 255]))

    def cook(self, pixels: np.ndarray):
        intensities = np.average(pixels, axis=2)
        indices = np.argsort(intensities)

        sorted_pixels = pixels[np.arange(len(pixels))[:, np.newaxis], indices]

        return sorted_pixels