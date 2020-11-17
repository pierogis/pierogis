import numpy as np

from pierogis.ingredients.ingredient import Ingredient

class Sort(Ingredient):

    def prep(self, **kwargs):
        self.target = kwargs.get('target')
        self.delimiter = kwargs.get('delimiter', np.array([255, 255, 255]))

    def cook(self, pixels: np.ndarray):
        mask = self.mask
        boolean_array = np.all(mask == self._white_pixel, axis=2)

        # false indicates that the pixel should not be sorted

        a = pixels[boolean_array]

        b = np.split(boolean_array)

        intensities = np.average(pixels, axis=2)
        a  =intensities[boolean_array]
        indices[boolean_array] = np.argsort(intensities[boolean_array])

        sorted_pixels = pixels[np.arange(len(pixels))[:, np.newaxis], indices[boolean_array]]

        return sorted_pixels