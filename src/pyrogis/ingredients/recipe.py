import numpy as np

from pyrogis.ingredients.ingredient import Ingredient


class Recipe(Ingredient):

    def prep(self, ingredients: list, **kwargs):
        """
        Provide a list of ingredients to cook in sequence

        :param ingredients: list of Ingredient objects
        """
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
            mixed_pixels = (
                                   cooked_pixels.astype(np.dtype(float)) * ingredient.opacity
                                   + under_pixels.astype(np.dtype(float)) * (100 - ingredient.opacity)
                           ) / 100
            # reset for loop
            under_pixels = mixed_pixels.astype('uint8')

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
