import numpy as np

from pierogis.ingredients.ingredient import Ingredient


class Recipe(Ingredient):

    def prep(self, ingredients: list, **kwargs):
        if ingredients is None:
            ingredients = []
        if isinstance(ingredients, list):
            self.ingredients = ingredients
        else:
            raise TypeError("kwarg 'ingredients' must be of type list")

    def cook(self, pixels: np.ndarray):
        """Applies pixels as a selection mask/base to ingredients
        """
        # input array used to select the
        under_pixels = pixels
        for ingredient in self.ingredients:
            # cook the lower layer
            cooked_pixels = ingredient.cook_mask(under_pixels)

            # mix them based on the overlaying opacity
            mixed_pixels = (cooked_pixels * ingredient.opacity + under_pixels * (100 - ingredient.opacity)) / 100

            # reset for loop
            under_pixels = mixed_pixels

        # keep in range
        clipped_pixels = np.clip(under_pixels, 0, 255)

        return clipped_pixels

    def add(self, ingredient: Ingredient):
        """
        Add an ingredient
        """
        self.ingredients.append(ingredient)

    # def select(self):
    #     self.pixel_array

    #     return Ingredient()
