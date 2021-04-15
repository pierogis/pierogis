import numpy as np

from .ingredient import Ingredient
from .seasonings.cartography import Direction
from .seasonings.rectangle import Rectangle


class Crop(Ingredient):
    """
    crop starting from an origin and selecting an area both defined as a compass direction
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
            origin: Direction = Rectangle.ORIGIN,
            **kwargs
    ) -> None:
        """
        :param x: 0 = left
        :param y: 0 = bottom
        :param width: width in pixels
        :param height: height in pixels
        :param aspect: aspect ratio to fill missing height or width (width/height, 1 means square)
        :param origin: location of origin for direction of crop select
        """
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.aspect = aspect
        self.origin = origin

    def cook(self, pixels: np.ndarray) -> np.ndarray:
        width = pixels.shape[0]
        height = pixels.shape[1]

        rectangle = Rectangle(
            width=self.width, height=self.height,
            x=self.x, y=self.y,
            aspect=self.aspect, origin=self.origin
        )

        bottom_left, top_right = rectangle.get_corner_coordinates(width, height)

        cooked_pixels = pixels[
                        bottom_left.x: top_right.x,
                        bottom_left.y: top_right.y
                        ]

        return cooked_pixels
