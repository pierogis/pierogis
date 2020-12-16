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

            mixed_pixels = (cooked_pixels * ingredient.opacity + under_pixels * (100 - ingredient.opacity)) / 100

            under_pixels = mixed_pixels

        clipped_pixels = np.clip(mixed_pixels, 0, 255)

        return clipped_pixels

    def add(self, ingredient: Ingredient):
        self.ingredients.append(ingredient)

    # def select(self):
    #     self.pixel_array

    #     return Ingredient()
