"""pierogi.py
"""

from PIL import Image
import numpy as np

from .ingredient import Ingredient


class Pierogi(Ingredient):
    """Image container for iterative pixel manipulation
    """

    def prep(self, image: Image=None, file: str=None):
        if not image:
            image = Image.open(file)

        self.pixels = np.array(image.convert('RGB'))

        # if self.height > 0 and self.width > 0:
        #     # truncate or fill pixels
        #     self.pixels = self.pixels.resize
        #     pass

    def cook(self, pixels: np.ndarray):
        """Return a cropped array of the image
        """

        pixels = self.pixels.reshape(pixels.shape).astype(pixels.dtype)
        return pixels
