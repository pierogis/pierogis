from typing import Tuple

import numpy as np

from .ingredient import Ingredient


class Crop(Ingredient):
    """
    crop starting from an origin and selecting an area in an ordinal direction

    :param origin: (0, 0) = bottom left
    :param width: width in pixels
    :param height: height in pixels
    :param aspect: aspect ratio to fill missing height/width from (width/height, 1 means square)

    """
    origin: Tuple[int, int]
    height: int
    width: int
    aspect: float

    def prep(
            self,
            origin: Tuple[int, int] = (0, 0),
            height: int = None,
            width: int = None,
            aspect: float = None,
            **kwargs
    ) -> None:
        """
        asdasd
        """
        self.origin = origin
        self.height = height
        self.width = width
        self.aspect = aspect

    def cook(self, pixels: np.ndarray) -> np.ndarray:
        width = pixels.shape[0]
        height = pixels.shape[1]

        if self.aspect is not None:
            aspect = self.aspect
        else:
            aspect = width / height

        if self.width is not None and self.height is not None:
            width = self.width
            height = self.height
        elif self.width is None and self.height is None:
            # neither provided, use aspect to smallenate the oversized dim
            if width / height > aspect:
                width = height * aspect
            else:
                height = width / aspect
        elif self.width is None:
            width = self.height * aspect
            height = self.height
        elif self.height is None:
            height = self.width / aspect
            width = self.width

        cooked_pixels = pixels[self.origin[0]: width, self.origin[1]: height]

        return cooked_pixels
