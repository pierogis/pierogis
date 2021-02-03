import numpy as np

from pyrogis import (
    Dish, Ingredient, Pierogi,
    Quantize, Recipe, Sort, Threshold
)

pierogi = Pierogi(path='gnome.jpg')


def threshold_example(self):
    threshold = Threshold(upper_threshold=100)

    # pass in lists to be mixed
    threshold_recipe = Recipe(ingredients=[pierogi, threshold])
    # recipe = Recipe(recipe)

    threshold_dish = Dish(
        height=pierogi.height,
        width=pierogi.width,
        recipe=threshold_recipe
    )

    threshold_dish.serve()


def swap_example(self):
    threshold = Threshold(target=pierogi, upper_threshold=200)

    swap_pixels = np.random.randint(0, 1, (10, 10, 3))
    swap = Ingredient(swap_pixels)
    threshold.season(swap)

    swap_recipe = Recipe(ingredients=[pierogi, swap])

    swap_dish = Dish(
        recipe=swap_recipe
    )

    swap_dish.serve()


def quantize_example(self):
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
    quantize_recipe = Recipe(ingredients=[pierogi, quantize])

    quantize_dish = Dish(
        recipe=quantize_recipe
    )

    quantize_dish.serve()


def sort_example(self):
    # threshold is a seasoning, which means it can be
    # used to add a mask to another Ingredient
    threshold = Threshold(target=pierogi, upper_threshold=80)

    sort = Sort()
    # apply a threshold mask to the sort
    threshold.season(sort)

    sort_recipe = Recipe(ingredients=[pierogi, sort])

    sort_dish = Dish(
        height=pierogi.height,
        width=pierogi.width,
        recipe=sort_recipe
    )

    sort_dish.serve()
    sort_dish.show()
