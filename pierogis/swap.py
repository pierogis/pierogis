import numpy as np

from .ingredient import Ingredient

class Swap(Ingredient):

    def prep(self, **kwargs):
        self.target = kwargs.get('target')
        self.select = kwargs.get('delimiter', np.array([255, 255, 255]))

    # def cook(self, pixels: np.ndarray):
    #     intensities = np.average(pixels, axis=2)
    #     indices = np.argsort(intensities)
    #
    #     sorted_pixels = pixels[np.arange(len(pixels))[:, np.newaxis], indices]
    #
    #     return sorted_pixels

    def cook(self, pixels: np.ndarray):
        delimiter_pixels = (pixels == self.select).all(axis=2)

        sorted_pixels = np.zeros(shape=(100, 100, 3))
        sorted_pixels[delimiter_pixels] = self.target.pixels[delimiter_pixels]



        return sorted_pixels