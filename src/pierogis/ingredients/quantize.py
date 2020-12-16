import typing

import numpy as np

from pierogis.ingredients.ingredient import Ingredient


class Quantize(Ingredient):
    def prep(self, palette: typing.Any = None):
        if palette is None:
            palette = [[0, 0, 0],
                       [255, 255, 255]]

        palette = np.array(palette)
        if palette.ndim != 2 or palette.shape[-1] != 3:
            raise ValueError('Palette should resizable to (n, 3)')

        self.palette = palette

    def cook(self, pixels: np.ndarray):
        a = np.expand_dims(pixels, axis=2)
        b = np.expand_dims(self.palette, axis=(0, 1))
        differences = np.expand_dims(pixels, axis=2) - np.expand_dims(self.palette, axis=(0, 1))

        distances = np.sqrt(np.sum(differences ** 2, axis=3))
        nearest_palette_index = np.argmin(distances, axis=2)

        return self.palette[nearest_palette_index]
