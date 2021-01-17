import numpy as np
from rpierogis import recipes

from pierogis.ingredients.ingredient import Ingredient


class Quantize(Ingredient):
    PALETTE_SIZE = 8
    ITERATIONS = 3
    REPEATS = 1
    INITIAL_TEMP = 1
    FINAL_TEMP = .001
    FILTER_SIZE = 3
    DITHERING_LEVEL = .8

    def prep(self,
             palette=None, palette_size=PALETTE_SIZE,
             iterations=ITERATIONS, repeats=REPEATS,
             initial_temp=INITIAL_TEMP, final_temp=FINAL_TEMP,
             dithering_level=DITHERING_LEVEL, seed=0):
        """
        Parameters for spatial color quantization
        """

        if palette is None:
            palette = np.empty((palette_size, 3))

        palette = np.array(palette)
        if palette.ndim != 2 or palette.shape[-1] != 3:
            raise ValueError('Palette should resizable to (n, 3)')

        self.palette = palette
        self.palette_size = palette_size
        self.iterations = iterations
        self.repeats = repeats
        self.initial_temp = initial_temp
        self.final_temp = final_temp
        self.filter_size = self.FILTER_SIZE
        self.dithering_level = dithering_level
        self.seed = seed

    def cook(self, pixels: np.ndarray):
        """
        Get the closest rgb color in the palette to each pixel rgb
        "Snap" to the colors in the palette
        """

        # rotating and unrotating because this library expects a different orientation
        cooked_pixels = np.rot90(recipes.quantize(
            np.ascontiguousarray(np.rot90(pixels), dtype=np.dtype('uint8')),
            palette_size=self.palette_size,
            iters_per_level=self.iterations,
            repeats_per_temp=self.repeats,
            initial_temp=self.initial_temp,
            final_temp=self.final_temp,
            filter_size=self.filter_size,
            dithering_level=self.dithering_level,
            seed=self.seed
        ), axes=(1,0))

        return cooked_pixels

    def cook_np(self, pixels: np.ndarray):
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

    @classmethod
    def add_parser_arguments(cls, parser):
        parser.add_argument('-p', '--palette', nargs='+',
                            help='hex color codes to quantize to')
        parser.add_argument('-n', '--palette_size', type=int, default=cls.PALETTE_SIZE,
                            help='number of colors in the palette')
        parser.add_argument('-i', '--iters', type=int, default=cls.ITERATIONS, dest='iterations',
                            help='iterations per coarseness level')
        parser.add_argument('-r', '--repeats', type=int, default=cls.REPEATS,
                            help='repeats per annealing temperature')
        parser.add_argument('--initial_temp', type=float, default=cls.INITIAL_TEMP,
                            help='repeats per annealing temperature')
        parser.add_argument('--final_temp', type=float, default=cls.FINAL_TEMP,
                            help='repeats per annealing temperature')
        parser.add_argument('-d', '--dithering_level', type=float, default=cls.DITHERING_LEVEL,
                            help='repeats per annealing temperature')
