import numpy as np

from pyrogis.ingredients import (
    Dish, Ingredient, Pierogi,
    Quantize, Recipe, Sort, Threshold
)

pierogi = Pierogi.from_path('gnome.jpg')


def threshold_example():
    threshold = Threshold(upper_threshold=100)

    # pass in lists to be mixed
    threshold_recipe = Recipe(ingredients=[threshold])
    # recipe = Recipe(recipe)

    threshold_dish = Dish(
        pierogi=pierogi,
        recipe=threshold_recipe
    )

    cooked_dish = threshold_dish.serve()

    cooked_dish.pierogi.show()


def swap_example():
    threshold = Threshold(target=pierogi, upper_threshold=200)

    swap_pixels = np.random.randint(0, 1, (10, 10, 3))
    swap = Ingredient(swap_pixels)
    swap.season(threshold)

    swap_recipe = Recipe(ingredients=[swap])

    swap_dish = Dish(
        pierogi=pierogi,
        recipe=swap_recipe
    )

    cooked_dish = swap_dish.serve()

    cooked_dish.pierogi.show()


def quantize_example():
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
    quantize_recipe = Recipe(ingredients=[quantize])

    quantize_dish = Dish(
        pierogi=pierogi,
        recipe=quantize_recipe
    )

    cooked_dish = quantize_dish.serve()

    cooked_dish.pierogi.show()


def sort_example():
    # threshold is a seasoning, which means it can be
    # used to add a mask to another Ingredient
    threshold = Threshold(target=pierogi, upper_threshold=80)

    sort = Sort()
    # apply a threshold mask to the sort
    sort.season(threshold)

    sort_recipe = Recipe(ingredients=[pierogi, sort])

    sort_dish = Dish(
        pierogi=pierogi,
        recipe=sort_recipe
    )

    cooked_dish = sort_dish.serve()

    cooked_dish.pierogi.show()


if __name__ == '__main__':
    sort_example()
