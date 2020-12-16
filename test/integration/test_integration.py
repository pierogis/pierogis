import numpy as np

from pierogis import Dish
from pierogis import Ingredient
from pierogis import Recipe
from pierogis import Pierogi
from pierogis import Quantize
from pierogis import Seasoning
from pierogis import Sort
from pierogis import Threshold


class TestDish():
    def test_threshold(self):
        pixels = np.random.randint(0, 255, (10, 15, 3))
        ingredient = Ingredient(pixels=pixels)
        ingredient.show()

        threshold = Threshold(upper_threshold=100)

        # pass in lists to be recipeed
        threshold_recipe = Recipe(ingredients=[ingredient, threshold])
        # recipe = Recipe(recipe)

        threshold_dish = Dish(height=ingredient.height, width=ingredient.width, recipe=threshold_recipe)

        threshold_dish.serve()
        threshold_dish.show()

    def test_season(self):
        pixels = np.random.randint(150, 255, (10, 10, 3))
        ingredient = Ingredient(pixels=pixels)

        threshold = Threshold(target=ingredient, upper_threshold=200)

        swap_pixels = np.random.randint(0, 1, (10, 10, 3))
        swap = Ingredient(swap_pixels)
        threshold.season(swap)

        swap_recipe = Recipe(ingredients=[ingredient, swap])

        swap_dish = Dish(height=ingredient.height, width=ingredient.width, recipe=swap_recipe)

        swap_dish.serve()

    def test_quantize(self):
        pixels = np.random.randint(0, 255, (10, 10, 3))
        ingredient = Ingredient(pixels=pixels)

        palette = [
            [100, 210, 69],
            [45, 23, 180],
            [62, 31, 70],
            [10, 210, 240],
            [45, 10, 244],
            [38, 31, 10],
            [255, 255, 255],
            [99, 94, 124]
        ]
        quantize = Quantize(palette=palette)

        # pass in lists to be mixed
        quantize_recipe = Recipe(ingredients=[ingredient, quantize])

        quantize_dish = Dish(height=ingredient.height, width=ingredient.width, recipe=quantize_recipe)

        quantize_dish.serve()

    def test_sort(self):
        pixels = np.random.randint(0, 255, (10, 10, 3))
        ingredient = Ingredient(pixels=pixels)

        # seasoning is for things that process but don't return a array
        threshold = Threshold(target=ingredient, upper_threshold=100)

        sort = Sort()
        # apply a threshold mask to the sort
        threshold.season(sort)

        sort_recipe = Recipe(ingredients=[ingredient, sort])

        sort_dish = Dish(height=ingredient.height, width=ingredient.width, recipe=sort_recipe)

        sort_dish.serve()
