import numpy as np

from .ingredient import Ingredient


class Recipe(Ingredient):
    """
    ingredient used to coordinate cooking of several ingredients

    when a recipe is cooked, its ingredients are cooked in order
    """

    def __call__(self, frame: int, frames: int):
        return self

    def prep(self, ingredients: list = None, **kwargs):
        """
        provide a list of ingredients to cook in sequence

        :param ingredients: list of Ingredient objects
        """
        if ingredients is None:
            ingredients = []
        if isinstance(ingredients, list):
            self.ingredients = ingredients
        else:
            raise TypeError("kwarg 'ingredients' must be of type list")

    def cook(self, pixels: np.ndarray):
        """
        sequentially cooks each ingredient
        uses the pixels resulting from the previous cook
        """
        # input array used to select the
        under_pixels = pixels
        for ingredient in self.ingredients:
            # cook the lower layer
            cooked_pixels = ingredient.cook(under_pixels)
            mask = ingredient.mask_pixels(cooked_pixels)
            binary_array = np.all(mask == self._white_pixel, axis=2)

            # resize under array to cooked array
            cooked_width = cooked_pixels.shape[0]
            cooked_height = cooked_pixels.shape[1]
            masked_pixels = np.resize(under_pixels, (cooked_width, cooked_height, 3))

            # layer cooked pixels over uncooked for true pixels (white in mask)
            masked_pixels[binary_array] = cooked_pixels[binary_array]

            # mix them based on the overlaying opacity
            mixed_pixels = (masked_pixels.astype(np.dtype(float))
                            * ingredient.opacity
                            +
                            under_pixels.astype(np.dtype(float))
                            * (100 - ingredient.opacity)) / 100
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
