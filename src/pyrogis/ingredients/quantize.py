import numpy as np
from PIL import ImageColor
from pierogis_rs import algorithms

from .ingredient import Ingredient


class Quantize(Ingredient):
    """
    quantize reduces the color palette of the input pixels to a smaller set.
    """

    def prep(self,
             colors=None, **kwargs):
        """
        parameters for spatial color quantization

        :param colors: colors to use. can be a list of str
        or pixel array likes
        """

        if colors is None:
            colors = np.asarray([[]])
        elif type(colors) is list:
            rgb_colors = []
            for color in colors:
                if type(color) is str:
                    if color[0] != '#':
                        color = '#' + color
                    rgb_colors.append(ImageColor.getcolor(color, "RGB"))

            colors = np.asarray(rgb_colors)

        else:
            colors = np.array(colors)

        self.palette = colors.astype(np.dtype('uint8'))
        """palette to use"""

    def cook(self, pixels: np.ndarray):
        """
        get the closest rgb color in the palette to each pixel rgb
        "snap" to the colors in the palette
        """
        # pixels -> (width, height, 1, 3)
        # palette -> (1, 1, n, 3)
        # subtract -> (width, height, n, 3)

        # the difference between pixel r, g, b (3) and color
        # for each pixel (width, height),
        # for each color in the palette (n, 3)
        differences = (
                np.expand_dims(pixels, axis=2)
                - np.expand_dims(self.palette, axis=(0, 1))
        )

        # sum up the last axis (r + g + b)
        # and sqrt that sum
        # -> (width, height, n)
        distances = np.sqrt(np.sum(differences ** 2, axis=3))

        # get the minimum among the n color
        # smallest value in each n group last dimension (smallest sqrt sum)
        # -> (width, height, 1)
        nearest_palette_index = np.argmin(distances, axis=2)

        # replace the min index identified with the corresponding color
        # -> (width, height, 3)
        return self.palette[nearest_palette_index]


class SpatialQuantize(Quantize):
    """
    use the Spatial Color Quantization algorithm
    implemented in rust with rscolorq

    also performs dithering to make the palette appear richer.
    """
    PALETTE_SIZE = 8
    ITERATIONS = 3
    REPEATS = 1
    INITIAL_TEMP = 1
    FINAL_TEMP = .001
    FILTER_SIZE = 3
    DITHERING_LEVEL = .8

    palette_size: int
    """number of colors"""
    iterations: int
    """number of iterations to do at each coarseness level"""
    repeats: int
    """number of repeats to do of each annealing temp"""
    initial_temp: float
    """starting annealing temp (around 1)"""
    final_temp: float
    """final annealing temp (decimal near but above 0)"""
    filter_size: int
    """filter size for dithering"""
    dithering_level: float
    """relative amount of dithering (.5-1.5)"""
    seed: int
    """seed for rng"""

    def prep(
            self, palette_size=PALETTE_SIZE,
            iterations=ITERATIONS, repeats=REPEATS,
            initial_temp=INITIAL_TEMP, final_temp=FINAL_TEMP,
            dithering_level=DITHERING_LEVEL, seed=0, **kwargs
    ):
        """

        """
        super().prep(**kwargs)

        self.palette_size = palette_size
        """number of colors"""
        self.iterations = iterations
        """number of iterations to do at each coarseness level"""
        self.repeats = repeats
        """number of repeats to do of each annealing temp"""
        self.initial_temp = initial_temp
        """starting annealing temp (around 1)"""
        self.final_temp = final_temp
        """final annealing temp (decimal near but above 0)"""
        self.filter_size = self.FILTER_SIZE
        self.dithering_level = dithering_level
        """relative amount of dithering (.5-1.5)"""
        self.seed = seed
        """seed for rng"""

    def cook(self, pixels: np.ndarray):
        """
        use the binding to the rscolorq package in rust
        to perform an optimization in quantizing and dithering
        """

        # rotating and unrotating because different orientation is expected
        cooked_pixels = np.rot90(algorithms.quantize(
            np.ascontiguousarray(np.rot90(pixels), dtype=np.dtype('uint8')),
            self.palette,
            palette_size=self.palette_size,
            iters_per_level=self.iterations,
            repeats_per_temp=self.repeats,
            initial_temp=self.initial_temp,
            final_temp=self.final_temp,
            filter_size=self.filter_size,
            dithering_level=self.dithering_level,
            seed=self.seed
        ), axes=(1, 0))

        return cooked_pixels
