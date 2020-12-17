# from abc import ABC
# from abc import abstractmethod

import numpy as np
from PIL import Image


class Ingredient:
    """
    Wrapper for a function to be applied to a grid of pixels.
    """

    # used to fill in empty spots when cooked
    _black_pixel = np.array([0, 0, 0])
    _white_pixel = np.array([255, 255, 255])

    default_pixel = _black_pixel

    def __init__(self, pixels: np.ndarray = None, origin: tuple = (0, 0), width: int = 0, height: int = 0,
                 opacity: int = 100, mask: np.ndarray = None, **kwargs):
        self.origin = origin
        self.opacity = opacity
        self.mask = mask

        if pixels is None:
            pixels = np.full((width, height, 3), self.default_pixel)

        self.pixels = pixels

        self.prep(**kwargs)

    @property
    def width(self):
        """
        From self.pixels
        """
        return self.pixels.shape[0]

    @property
    def height(self):
        """
        From self.pixels
        """
        return self.pixels.shape[1]

    # @property
    # def size(self):
    #     """(width, height)
    #     """
    #     return self.width, self.height

    @property
    def shape(self):
        """
        (width, height, 3)
        """
        return self.width, self.height, 3

    def prep(self, *args, **kwargs):
        """
        Parameterize the cook function
        """
        pass

    def get_image(self):
        """
        Turn the numpy array into a PIL Image
        """
        image = Image.fromarray(np.rot90(self.pixels), 'RGB')
        return image

    def cook(self, pixels: np.ndarray):
        """
        Performs actions on a pixel array and returns a cooked array
        """
        return self.pixels

    def apply_mask(self, uncooked_pixels, cooked_pixels):
        """
        Only apply the cook for white pixels in the mask
        """
        # use uncooked pixels as base
        masked_pixels = np.copy(uncooked_pixels)

        mask = self.mask
        if mask is None:
            # all True
            binary_array = np.full(cooked_pixels.shape[:2], True)
        else:
            # True if white
            binary_array = np.all(mask == self._white_pixel, axis=2)

        # layer cooked pixels over uncooked for true pixels (white in mask)
        masked_pixels[binary_array] = cooked_pixels[binary_array]

        return masked_pixels

    def cook_mask(self, pixels: np.ndarray):
        """
        Cook the pixels, then apply the ingredient's mask
        """
        cooked_pixels = self.cook(pixels)
        masked_pixels = self.apply_mask(pixels, cooked_pixels)
        return masked_pixels

    def show(self):
        """
        Open the image view to display the array
        """
        self.get_image().show()
