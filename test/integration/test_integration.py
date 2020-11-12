import unittest

from pierogis import Pierogi
from pierogis import Threshold
# from pierogis import Recipe
from pierogis import Mix
from pierogis import Dish
from pierogis import Sort


class TestDish(unittest.TestCase):
    def test_threshold(self):
        image_path = '/Users/kyle/Desktop/input1.png'
        pierogi = Pierogi(file=image_path)

        threshold = Threshold()

        # pass in lists to be mixed
        mix = Mix(ingredients=[pierogi, threshold])
        # recipe = Recipe(mix)

        dish = Dish(mix=mix, height=pierogi.height, width=pierogi.width)

        dish.serve()
        dish.show()

    def test_sort(self):
        image_path = '/Users/kyle/Desktop/input1.png'
        pierogi = Pierogi(file=image_path)

        # pass in lists to be mixed
        sort = Sort(ingredient=pierogi)
        mix = Mix(ingredients=[pierogi, sort])

        dish = Dish(mix=mix, height=pierogi.height, width=pierogi.width)

        dish.serve()
        dish.show()

if __name__ == '__main__':
    unittest.main()
