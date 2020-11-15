import numpy as np

from pierogis import Dish
from pierogis import Ingredient
from pierogis import Interval
# from pierogis import Recipe
from pierogis import Mix
from pierogis import Pierogi
from pierogis import Quantize
from pierogis import Seasoning
from pierogis import Sort
from pierogis import Swap
from pierogis import Threshold


class TestDish():
    def test_threshold(self):
        image_path = '/Users/kyle/Desktop/input1.png'
        pierogi = Pierogi()
        pierogi.prep(file=image_path)

        threshold = Threshold()
        threshold.prep()

        # pass in lists to be mixed
        threshold_mix = Mix()
        threshold_mix.prep([pierogi, threshold])
        # recipe = Recipe(mix)

        threshold_dish = Dish(height=pierogi.height, width=pierogi.width)
        threshold_dish.prep(threshold_mix)

        threshold_dish.serve()

    def test_swap(self):
        image_path = '/Users/kyle/Desktop/input/IMG_1832.png'
        pierogi = Pierogi(file=image_path)

        threshold = Threshold(upper_threshold=50)

        # pass in lists to be mixed
        threshold_mix = Mix(ingredients=[pierogi, threshold])
        # recipe = Recipe(mix)

        threshold_dish = Dish(mix=threshold_mix, height=pierogi.height, width=pierogi.width)

        threshold_dish.serve()

        # pass in lists to be mixed
        swap = Swap(target=pierogi)

        mix = Mix(ingredients=[pierogi, threshold, swap])

        swap_dish = Dish(mix=mix, height=pierogi.height, width=pierogi.width)

        swap_dish.serve()
        swap_dish.show()

    def test_quantize(self):
        image_path = '/Users/kyle/Desktop/input/EfHFNHNXYAARqmi.jpg'
        pierogi = Pierogi(file=image_path)

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

        # quantize.season(palette=palette)

        # pass in lists to be mixed
        quantize_mix = Mix(ingredients=[pierogi, quantize])
        # recipe = Recipe(mix)

        quantize_dish = Dish(mix=quantize_mix, height=pierogi.height, width=pierogi.width)

        quantize_dish.serve()
        quantize_dish.show()

    def test_sort(self):
        pixels = np.random.randint(0, 255, (4, 4, 3))
        ingredient = Ingredient(pixels=pixels)

        threshold = Threshold(upper_threshold=100)
        threshold_mix = Mix(ingredients=[ingredient, threshold])
        threshold_dish = Dish(mix=threshold_mix, height=ingredient.height, width=ingredient.width)

        threshold_dish.serve()

        # seasoning is for things that process but don't return a array
        seasoning = Seasoning(target=threshold_dish)

        sort = Sort()
        # this will call a function on each kwarg and set the return to the sort's attribute with the name of the kwarg
        sort.season(seasoning)

        sort_mix = Mix(ingredients=[ingredient, threshold, sort])

        sort_dish = Dish(mix=sort_mix, height=ingredient.height, width=ingredient.width)

        sort_dish.serve()
        sort_dish.show()
