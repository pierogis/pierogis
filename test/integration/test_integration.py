import unittest

from pierogis import Pierogi
from pierogis import Threshold
# from pierogis import Recipe
from pierogis import Mix
from pierogis import Dish


class TestDish(unittest.TestCase):
    def test_serve(self):
        image_path = '/Users/kyle/Desktop/input1.png'
        pierogi = Pierogi(image=image_path)

        threshold = Threshold(lower_threshold=100, upper_threshold=120)

        # pass in lists to be mixed
        mix = Mix(ingredients=[pierogi, threshold])
        # recipe = Recipe(mix)

        dish = Dish(mix, size=pierogi.size)

        for pierogi in dish.serve():
            cooked_pierogi = pierogi
            pass

        bites = cooked_pierogi.to_bytes()

        cooked_image = Image.frombytes("RGBA", image.size, bites)

        cooked_image.show()
        pierogi.show()


if __name__ == '__main__':
    unittest.main()
