import numpy as np

from .ingredient import Ingredient
from .pierogi import Pierogi
from .recipe import Recipe


class Dish(Ingredient):
    """
    cook a pierogi with a recipe
    """

    _pierogi: Pierogi = None

    def prep(
            self,
            pierogi: Pierogi,
            recipe: Recipe = None,
            **kwargs
    ):
        """
        set the recipe to cook for this dish

        :param recipe: something callable that returns a
        cook(pixels) method.
        Any Ingredient (including recipe) is an example of this

        :param pierogis: a list of Pierogi to cook
        """
        self.pierogi = pierogi

        if recipe is None:
            recipe = Recipe()
        self.recipe = recipe

    def cook(self, pixels: np.ndarray) -> np.ndarray:
        return self.recipe.cook(self.pierogi.pixels)

    def serve(self) -> 'Dish':
        """
        cook the recipe and set the output to this object's pixel array
        """

        # cook with these pixels as first input
        cooked_pixels = self.recipe.cook(self.pierogi.pixels)
        # ensure that the cooked pixels do not overflow 0-255
        clipped_pixels = np.clip(cooked_pixels, 0, 255)
        # # set the objects own pixels to the result of cooking
        cooked_pierogi = Pierogi(pixels=clipped_pixels)

        return Dish(pierogi=cooked_pierogi)
