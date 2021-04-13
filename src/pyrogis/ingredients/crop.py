import numpy as np

from .ingredient import Ingredient


class Crop(Ingredient):
    """
    crop starting from an origin and selecting an area in an ordinal direction
    """
    X = 0
    Y = 0

    x: int
    y: int
    height: int
    width: int
    aspect: float

    def prep(
            self,
            x: int = X,
            y: int = Y,
            height: int = None,
            width: int = None,
            aspect: float = None,
            **kwargs
    ) -> None:
        """
        :param x: 0 = left
        :param y: 0 = bottom
        :param width: width in pixels
        :param height: height in pixels
        :param aspect: aspect ratio to fill missing height/width from (width/height, 1 means square)
        """
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.aspect = aspect

    def cook(self, pixels: np.ndarray) -> np.ndarray:
        width = pixels.shape[0]
        height = pixels.shape[1]

        if self.width is not None and self.height is not None:
            width = self.width
            height = self.height
        elif self.width is None and self.height is None:
            # neither provided, use aspect to smallenate the oversized dim
            if self.aspect is not None:
                if width / height > self.aspect:
                    width = height * self.aspect
                else:
                    height = width / self.aspect
        elif self.width is None:
            if self.aspect is not None:
                aspect = self.aspect
                width = self.height * aspect

            height = self.height
        elif self.height is None:
            if self.aspect is not None:
                aspect = self.aspect
                height = self.width / aspect

            width = self.width

        cooked_pixels = pixels[
                        self.x: self.x + round(width),
                        self.y: self.y + round(height)
                        ]

        return cooked_pixels
