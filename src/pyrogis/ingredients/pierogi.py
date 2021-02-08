"""
define an image wrapper ingredient
"""
import os

import imageio
import numpy as np
from PIL import Image

from .ingredient import Ingredient


class Pierogi(Ingredient):
    """
    image container for iterative pixel manipulation

    uses PIL.Image to load to self.pixels
    """

    @property
    def image(self):
        """
        turn the numpy array into a PIL Image
        """
        image = Image.fromarray(np.rot90(self.pixels), 'RGB')
        return image

    def prep(
            self,
            pixels: np.ndarray = None,
            shape: tuple = (0, 0),
            image: Image = None,
            file: str = None,
            **kwargs
    ):
        """
        provide the source image in a number of ways

        :param pixels: numpy array
        :param image: PIL Image that has already been loaded
        :param file: provide an input image as a file
        :param file: file path to load from
        """

        if pixels is None:
            if image is not None:
                # rotate the image array on receipt so that
                # array dimensions are (width, height, 3)
                pixels = np.rot90(np.array(image.convert('RGB')), axes=(1, 0))
            elif file is not None:
                self.file = file
                pixels = np.rot90(np.array(imageio.imread(file)), axes=(1, 0))
            elif shape is not None:
                pixels = np.full((*shape, 3), self.default_pixel)
            else:
                raise Exception("one of image, file, or shape must be provided")

        self.pixels = pixels

    def cook(self, pixels: np.ndarray):
        """
        performs actions on a pixel array and returns a cooked array
        """
        return self.pixels

    def show(self):
        """
        open an image viewer to display the array
        """
        self.image.show()

    def save(self, path, optimize=False):
        """
        save the image to the given path
        """

        output_filename = path
        if os.path.isdir(path):
            output_filename = os.path.join(
                path, os.path.split(self.file)[1]
            )

        self.image.save(output_filename, optimize=optimize)
