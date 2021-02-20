import numpy as np
import pytest

from pyrogis import Dish, Pierogi


@pytest.fixture
def array():
    return np.asarray([[[200, 200, 200], [30, 30, 30]],
                       [[130, 130, 130], [60, 60, 60]]]).astype(np.dtype('uint8'))


def test_dish_1(array):
    pierogi = Pierogi(pixels=array)

    dish = Dish(pierogis=[pierogi])

    assert np.all(dish.pierogis[0] == pierogi)


def test_dish_2(array):
    pierogi = Pierogi(pixels=array)
    pierogi2 = Pierogi(pixels=np.rot90(array))

    dish = Dish(pierogis=[pierogi, pierogi2])

    assert np.all(dish.pierogis[1] == pierogi2)
