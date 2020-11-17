import numpy as np

from pierogis import Dish
from pierogis import Ingredient
from pierogis import Mix
from pierogis import Pierogi
from pierogis import Quantize
from pierogis import Seasoning
from pierogis import Sort
from pierogis import Threshold


class TestDish():
    def test_threshold(self):
        pixels = np.random.randint(0, 255, (10, 10, 3))
        ingredient = Ingredient(pixels=pixels)

        threshold = Threshold()
        threshold.prep(upper_threshold=100)

        # pass in lists to be mixed
        threshold_mix = Mix()
        threshold_mix.prep([ingredient, threshold])
        # recipe = Recipe(mix)

        threshold_dish = Dish(height=ingredient.height, width=ingredient.width)
        threshold_dish.prep(threshold_mix)

        threshold_dish.serve()

    def test_season(self):
        pixels = np.random.randint(150, 255, (10, 10, 3))
        ingredient = Ingredient(pixels=pixels)

        threshold = Threshold(target=ingredient)
        threshold.prep(upper_threshold=200)

        swap_pixels = np.random.randint(0, 1, (10, 10, 3))
        swap = Ingredient(swap_pixels)
        threshold.season(swap)

        swap_mix = Mix()
        swap_mix.prep(ingredients=[ingredient, swap])

        swap_dish = Dish(height=ingredient.height, width=ingredient.width)
        swap_dish.prep(mix=swap_mix)

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
        quantize = Quantize()
        quantize.prep(palette=palette)

        # quantize.season(palette=palette)

        # pass in lists to be mixed
        quantize_mix = Mix()
        quantize_mix.prep(ingredients=[ingredient, quantize])
        # recipe = Recipe(mix)

        quantize_dish = Dish(height=ingredient.height, width=ingredient.width)
        quantize_dish.prep(mix=quantize_mix)

        quantize_dish.serve()

    def test_sort(self):
        pixels = np.random.randint(0, 255, (10, 10, 3))
        ingredient = Ingredient(pixels=pixels)

        # seasoning is for things that process but don't return a array
        threshold = Threshold(target=ingredient)
        threshold.prep(upper_threshold=100)

        sort = Sort()
        # apply a threshold mask to the sort
        threshold.season(sort)

        sort_mix = Mix()
        sort_mix.prep(ingredients=[ingredient, sort])

        sort_dish = Dish(height=ingredient.height, width=ingredient.width)
        sort_dish.prep(mix=sort_mix)

        sort_dish.serve()
        sort_dish.show()
