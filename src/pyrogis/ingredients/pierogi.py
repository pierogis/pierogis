"""pierogi.py
"""
import io

from PIL import Image
import numpy as np

from .ingredient import Ingredient


class Pierogi(Ingredient):
    """
    Image container for iterative pixel manipulation

    Uses PIL.Image to load to self.pixels
    """

    def prep(self, image: Image = None, file: str = None):
        """
        Provide either a PIL Image or a path to an image file

        :param image: Provide a PIL Image that has already been loaded (takes precedence)
        :param file: Provide a file path to load from
        """
        if not image:
            image = Image.open(file)

        # rotate the image array on receipt so that the array dimensions are (width, height, 3)
        self.pixels = np.rot90(np.array(image.convert('RGB')), axes=(1, 0))

        # if self.height > 0 and self.width > 0:
        #     # truncate or fill pixels
        #     self.pixels = self.pixels.resize
        #     pass

    def cook(self, pixels: np.ndarray):
        """
        Return a reshaped array of the image
        """

        return self.pixels.reshape(pixels.shape).astype(pixels.dtype)
