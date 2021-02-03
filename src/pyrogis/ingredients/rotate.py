import numpy as np

from .ingredient import Ingredient


class Rotate(Ingredient):
    """
    rotate a pixel array
    """

    def prep(self, clockwise: bool = True, turns: int = 1, **kwargs):
        """
        provide a given number of turns in a specified direction

        :param clockwise if True, top left pixel becomes top right
        :param turns number of 90 degree turns to make
        """
        self.clockwise = clockwise
        self.turns = turns

    def cook(self, pixels: np.ndarray):
        """
        rotate the pixels according to parameters
        """
        rotated_pixels = pixels
        # determine axes of rotation from clockwise or not
        rotation_axes = (0, 1) if self.clockwise else (1, 0)

        # turn turns number of times
        for i in range(self.turns):
            rotated_pixels = np.rot90(rotated_pixels, axes=rotation_axes)

        return rotated_pixels

    @classmethod
    def unrotate(cls, rotate: 'Rotate'):
        """
        return a Rotate that will reverse the given Rotate

        :param rotate the rotate to reverse
        """
        return cls(clockwise=not rotate.clockwise, turns=rotate.turns)
