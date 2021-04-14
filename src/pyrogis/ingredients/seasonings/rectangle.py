from typing import Union, Tuple

import numpy as np

from .cartography import Direction, Coordinate
from .seasoning import Seasoning


class Rectangle(Seasoning):
    width: Union[int, float]
    height: Union[int, float]
    x: Union[int, float]
    y: Union[int, float]
    aspect: float
    origin: Direction

    ORIGIN: Direction = Direction.SW

    def prep(
            self,
            width: Union[int, float] = None, height: Union[int, float] = None,
            x: Union[int, float] = 0, y: Union[int, float] = 0,
            aspect: float = None, origin: Direction = ORIGIN,
            **kwargs
    ):
        super().prep(**kwargs)

        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.aspect = aspect
        self.origin = origin

    def cook(self, pixels: np.ndarray):
        # create an array of all excludes

        boolean_array = np.zeros(pixels.shape[:2], dtype=bool)

        bottom_left, top_right = self.get_corner_coordinates(pixels.shape[0], pixels.shape[1])

        boolean_array[bottom_left.x:top_right.x, bottom_left.y:top_right.y] = True

        boolean_array = np.expand_dims(boolean_array, 2)

        binary_pixels = np.where(
            boolean_array, self.include_pixel, self.exclude_pixel
        )

        return binary_pixels

        # include all pixels that are inside of the bounding coords

    def get_corner_coordinates(
            self, bounding_width: int, bounding_height: int
    ) -> Tuple[Coordinate, Coordinate]:
        # x, y for bottom left and top right

        if self.origin is Direction.SW:
            x = 0
            y = 0
            bl_x_multiplier = 0
            tr_x_multiplier = 1
            bl_y_multiplier = 0
            tr_y_multiplier = 1

        elif self.origin is Direction.SE:
            x = bounding_width
            y = 0
            bl_x_multiplier = 1
            tr_x_multiplier = 0
            bl_y_multiplier = 0
            tr_y_multiplier = 1

        elif self.origin is Direction.NW:
            x = 0
            y = bounding_height
            bl_x_multiplier = 0
            tr_x_multiplier = 1
            bl_y_multiplier = 1
            tr_y_multiplier = 0

        elif self.origin is Direction.NE:
            x = bounding_width
            y = bounding_height
            bl_x_multiplier = 1
            tr_x_multiplier = 0
            bl_y_multiplier = 1
            tr_y_multiplier = 0

        elif self.origin is Direction.C:
            x = bounding_width * .5
            y = bounding_height * .5
            bl_x_multiplier = .5
            tr_x_multiplier = .5
            bl_y_multiplier = .5
            tr_y_multiplier = .5

        elif self.origin is Direction.N:
            x = bounding_width * .5
            y = bounding_height
            bl_x_multiplier = .5
            tr_x_multiplier = .5
            bl_y_multiplier = 1
            tr_y_multiplier = 0

        elif self.origin is Direction.E:
            x = bounding_width
            y = bounding_height * .5
            bl_x_multiplier = 1
            tr_x_multiplier = 0
            bl_y_multiplier = .5
            tr_y_multiplier = .5

        elif self.origin is Direction.S:
            x = bounding_width * .5
            y = 0
            bl_x_multiplier = .5
            tr_x_multiplier = .5
            bl_y_multiplier = 0
            tr_y_multiplier = 1

        elif self.origin is Direction.W:
            x = 0
            y = bounding_height * .5
            bl_x_multiplier = 0
            tr_x_multiplier = 1
            bl_y_multiplier = .5
            tr_y_multiplier = .5

        else:
            raise Exception()

        if self.x != 0:
            if 1 > self.x > -1:
                x += self.x * bounding_width
            else:
                x += self.x

        if self.y != 0:
            if 1 > self.y > -1:
                y += self.y * bounding_height
            else:
                y += self.y

        origin = Coordinate(x, y)

        width = None
        height = None

        if self.width is not None:
            width = self.width
            if 1 > width > -1:
                width *= bounding_width

        if self.height is not None:
            height = self.height
            if 1 > height > -1:
                height *= bounding_height

        if not (self.width is not None and self.height is not None):
            if self.width is not None:
                if self.aspect is not None:
                    height = width / self.aspect
                else:
                    height = bounding_height
            elif self.height is not None:
                if self.aspect is not None:
                    width = height * self.aspect
                else:
                    width = bounding_width

            else:
                width = bounding_width
                height = bounding_height

                if self.aspect is not None:
                    if width / height > self.aspect:
                        width = height * self.aspect
                    else:
                        height = width / self.aspect

        bl_x = int(origin.x - bl_x_multiplier * width)
        if bl_x < 0:
            bl_x = 0

        bl_y = int(origin.y - bl_y_multiplier * height)
        if bl_y < 0:
            bl_y = 0

        tr_x = int(origin.x + tr_x_multiplier * width)
        if tr_x > bounding_width:
            tr_x = bounding_width

        tr_y = int(origin.y + tr_y_multiplier * height)
        if tr_y > bounding_height:
            tr_y = bounding_height

        bottom_left = Coordinate(
            bl_x,
            bl_y
        )
        top_right = Coordinate(
            tr_x,
            tr_y
        )

        return bottom_left, top_right
