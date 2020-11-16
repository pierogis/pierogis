import numpy as np

from pierogis.ingredients.ingredient import Ingredient


class Quantize(Ingredient):
    def prep(self, **kwargs):
        self.palette = kwargs.get('palette', [[0, 0, 0],
                                              [255, 255, 255]])

    def cook(self, pixels: np.ndarray):
        palette = np.array(self.palette)
        differences = np.expand_dims(pixels, axis=2) - np.expand_dims(palette, axis=(0, 1))

        distances = np.sqrt(np.sum(differences ** 2, axis=3))
        nearest_palette_index = np.argmin(distances, axis=2)

        return palette[nearest_palette_index]
