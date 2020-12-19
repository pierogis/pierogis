"""pierogi.py
"""
import io

from PIL import Image
import numpy as np

from .ingredient import Ingredient


class Pierogi(Ingredient):
    """
    Image container for iterative pixel manipulation
    """

    def prep(self, image: Image = None, path: str = None):
        """
        Provide either a PIL Image or a path to an image file
        """
        if not image:
            image = Image.open(path)

        # rotate the image array on receipt so that the array dimensions are (width, height, 3)
        self.pixels = np.rot90(np.array(image.convert('RGB')), axes=(1, 0))

        # if self.height > 0 and self.width > 0:
        #     # truncate or fill pixels
        #     self.pixels = self.pixels.resize
        #     pass

    def cook(self, pixels: np.ndarray):
        """
        Return a cropped array of the image
        """

        return self.pixels.reshape(pixels.shape).astype(pixels.dtype)
