import numpy as np

from pierogis.ingredients.ingredient import Ingredient

class Sort(Ingredient):

    def prep(self, **kwargs):
        self.target = kwargs.get('target')
        self.delimiter = kwargs.get('delimiter', np.array([255, 255, 255]))

    # def cook(self, pixels: np.ndarray):
    #     mask = self.mask
    #     boolean_array = np.all(mask == self._white_pixel, axis=2)
    #
    #     # false indicates that the pixel should not be sorted
    #
    #     intensities = np.average(pixels, axis=2)
    #     indices = np.argsort(intensities)
    #
    #     sorted_pixels = pixels[np.arange(len(pixels))[:, np.newaxis], indices]
    #
    #     return sorted_pixels

    def cook(self, pixels: np.ndarray):
        mask = self.mask
        boolean_array = np.all(mask == self._white_pixel, axis=2)
        # false indicates that the pixel should not be sorted

        intensities = np.average(pixels, axis=2)
        start = 0
        end = 3
        j = 0
        ind = np.array([[0]])
        a = intensities[ind]
        intensities[ind] = np.sort(intensities[ind])

        indices = np.argsort(intensities)

        sorted_pixels = pixels[np.arange(len(pixels))[:, np.newaxis], indices]

        return sorted_pixels