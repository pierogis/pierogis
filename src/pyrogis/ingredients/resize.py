import numpy as np

from .ingredient import Ingredient
from .pierogi import Pierogi


class Resize(Ingredient):
    """
    resize using width, height, and scale
    """

    def prep(
            self,
            width: int = None,
            height: int = None,
            scale: int = 1,
            resample: int = Pierogi.RESAMPLE,
            **kwargs
    ):
        """
        if only one of width and height is provided,
        aspect ratio will be maintained.

        when reducing size,
        a dimension will round down if it would be a decimal

        cook 5x5 pixels prepped with a .5 scale -> resized to 2x2
        cook 2x3 pixels prepped with a width of 1 -> resized to 1x1

        :param width: width to resize to
        :param height: height to resize to
        :param scale: scale multiplier (2 means 2x)
        :param resample: resample filter to use
        """

        if width is None and height is None and scale is None:
            ValueError("One of width height or scale must be provided")

        self.width = width
        self.height = height
        self.scale = scale
        self.resample = resample

    def cook(self, pixels: np.ndarray):
        pierogi = Pierogi(pixels=pixels)

        width = pixels.shape[0]
        height = pixels.shape[1]

        if self.width is not None and self.height is not None:
            width = self.width
            height = self.height
        else:
            if self.width is not None or self.height is not None:
                aspect = width / height

                if self.width is None:
                    width = self.height * aspect
                    height = self.height
                elif self.height is None:
                    height = self.width / aspect
                    width = self.width

        width *= self.scale
        height *= self.scale

        pierogi.resize(int(width), int(height), self.resample)

        return pierogi.pixels
