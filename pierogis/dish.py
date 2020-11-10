import numpy as np

from .ingredient import Ingredient
from .mix import Mix

class Dish(Ingredient):
    """Cook an entire recipe for all pixels
    """
    
    def __init__(self, mix: Mix, **kwargs):
        super().__init__(**kwargs)
        self.mix = mix

    def serve(self):
        if self.size == (0, 0):
            base = self.mix.ingredients[0]
            self.width, self.height = base.size

            self.pixels = np.full((self.width, self.height), self.default_pixel)

        for x in range(self.width):
            for y in range(self.height):
                for pixel in self.mix.cook(self.pixels[x][y], x, y):
                    self.pixels[x][y] = pixel

    # taste test - serve and cook each ingredient simulatneously