"""Add a seasoning to an ingredient before you cook it
"""

from abc import ABC
from abc import abstractmethod

import numpy as np

from .ingredient import Ingredient


class Seasoning(Ingredient):
    """Seasonings perform their computation in the prep stage.
    They are different from an ingredient because the outcome of
    their processing is not equal in size to the input array

    Seasonings are masks that use their season function to generate
    a selection of pixels to be operated on by the cook operation.

    They can be put into a mix to define a mask for a default
    target.pixels.shape sized "all passing" pixels.shape array.
    The can also be added to an ingredient through
    Ingredient.season.
    """

    def prep(self, target: Ingredient, delimiter: np.ndarray=np.array([255, 255, 255])):
        self.target = target
        self.delimiter = delimiter

    def season(self):
        return self.cook(self.target.pixels)

    def cook(self, pixels: np.ndarray):
        a = np.all(self.target.pixels == self.delimiter, axis=2)

        b = np.where(a, np.array([0, 0, 0]), np.array([255, 255, 255]))
        return b
