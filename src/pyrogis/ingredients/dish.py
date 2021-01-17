import numpy as np

from pyrogis.ingredients.ingredient import Ingredient
from pyrogis.ingredients.recipe import Recipe


class Dish(Ingredient):
    """
    Crop and cook an entire recipe for all pixels
    """

    def prep(self, recipe: Recipe):
        """
        Set the recipe to cook for this dish

        :param recipe: Recipe to cook and serve
        """
        self.recipe = recipe

    def cook(self, pixels: np.ndarray):
        """
        Use the recipe's cook_mask() method
        """
        return self.recipe.cook_mask(pixels)

    def serve(self):
        """
        Cook the recipe and set the output to this object's pixel array
        """

        pixels = self.pixels

        # if pixels weren't provided, create a blank canvas sized to the first element of the mix
        if pixels.shape == (0, 0, 3):
            base = self.recipe.ingredients[0]
            pixels = base.pixels

        # cook with these pixels as first input
        cooked_pixels = self.cook(pixels)
        # ensure that the cooked pixels do not overflow 0-255
        clipped_pixels = np.clip(cooked_pixels, 0, 255)

        # set the objects own pixels to the result of cooking
        ingredient = Ingredient(pixels=clipped_pixels)

        return ingredient
