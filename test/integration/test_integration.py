import unittest

from pierogis import Pierogi
from pierogis import Threshold
# from pierogis import Recipe
from pierogis import Mix
from pierogis import Dish
from pierogis import Sort
from pierogis import Interval
from pierogis import Swap


class TestDish(unittest.TestCase):
    def test_threshold(self):
        image_path = '/Users/kyle/Desktop/input1.png'
        pierogi = Pierogi(file=image_path)

        threshold = Threshold()

        # pass in lists to be mixed
        threshold_mix = Mix(ingredients=[pierogi, threshold])
        # recipe = Recipe(mix)

        threshold_dish = Dish(mix=threshold_mix, height=pierogi.height, width=pierogi.width)

        threshold_dish.serve()

    def test_swap(self):
        image_path = '/Users/kyle/Desktop/input1.png'
        pierogi = Pierogi(file=image_path)

        threshold = Threshold()

        # pass in lists to be mixed
        threshold_mix = Mix(ingredients=[pierogi, threshold])
        # recipe = Recipe(mix)

        threshold_dish = Dish(mix=threshold_mix, height=pierogi.height, width=pierogi.width)

        threshold_dish.serve()

        image_path = '/Users/kyle/Desktop/input1.png'
        pierogi = Pierogi(file=image_path)

        interval = Interval(target=threshold_dish)

        # pass in lists to be mixed
        swap = Swap(target=pierogi)
        swap.season(interval)

        mix = Mix(ingredients=[pierogi, threshold, swap])

        dish = Dish(mix=mix, height=pierogi.height, width=pierogi.width)

        dish.serve()
        dish.show()


if __name__ == '__main__':
    unittest.main()
