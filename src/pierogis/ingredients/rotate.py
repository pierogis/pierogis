from typing import Union

import numpy as np
from PIL import Image

from .ingredient import Ingredient
from .pierogi import Pierogi


class Rotate(Ingredient):
    """rotate a pixel array"""
    DEFAULT_RESAMPLE = 'nearest'
    FILTERS = {
        'nearest': Image.NEAREST,
        'box': Image.BOX,
        'bicubic': Image.BICUBIC,
        'bilinear': Image.BILINEAR,
        'hamming': Image.HAMMING,
        'lanczos': Image.LANCZOS,
    }

    def prep(
            self,
            clockwise: bool = True, turns: int = 1, angle: int = 90,
            resample: Union[int, str] = FILTERS[DEFAULT_RESAMPLE],
            **kwargs
    ):
        """
        provide a given number of turns in a specified direction

        :param clockwise: if True, top left pixel becomes top right
        :param turns: number of "angle" degree turns to make
        :param angle: distance to turn
        :param resample: resample filter to use
        """
        self.angle = angle
        self.clockwise = clockwise
        self.turns = turns
        self.resample = resample

    def cook(self, pixels: np.ndarray):
        """rotate the pixels according to angle"""
        pierogi = Pierogi(pixels=pixels)

        angle = self.turns * self.angle
        if self.clockwise:
            angle *= -1

        resample = self.resample
        if (isinstance(resample, str)):
            resample = self.FILTERS[resample]

        pierogi.rotate(angle, resample)

        return pierogi.pixels

    @classmethod
    def unrotate(cls, rotate: 'Rotate'):
        """
        return a Rotate that will reverse the given Rotate

        :param rotate: the rotate to reverse
        """
        return cls(
            angle=rotate.angle, clockwise=not rotate.clockwise, turns=rotate.turns, resample=rotate.resample
        )
