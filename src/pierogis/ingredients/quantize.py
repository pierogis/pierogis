import typing

import numpy as np

from pierogis.ingredients.ingredient import Ingredient


class Quantize(Ingredient):
    def prep(self, palette=None):
        if palette is None:
            palette = [[0, 0, 0],
                       [255, 255, 255]]

        palette = np.array(palette)
        if palette.ndim != 2 or palette.shape[-1] != 3:
            raise ValueError('Palette should resizable to (n, 3)')

        self.palette = palette

    def cook(self, pixels: np.ndarray):
        """
        Get the closest rgb color in the palette to each pixel rgb
        "Snap" to the colors in the palette
        """

        # pixels -> (width, height, 1, 3)
        # palette -> (1, 1, n, 3)
        # subtract -> (width, height, n, 3)

        # the difference between pixel r, g, b (3) and color
        # for each pixel (width, height),
        # for each color in the palette (n, 3)
        differences = np.expand_dims(pixels, axis=2) - np.expand_dims(self.palette, axis=(0, 1))

        # sum up the last axis (r + g + b)
        # and sqrt that sum
        # -> (width, height, n)
        distances = np.sqrt(np.sum(differences ** 2, axis=3))

        # get the minimum among the n color
        # smallest value in each n group in the last dimension (smallest sqrt sum)
        # -> (width, height, 1)
        nearest_palette_index = np.argmin(distances, axis=2)

        # replace the min index identified with the corresponding color
        # -> (width, height, 3)
        return self.palette[nearest_palette_index]
