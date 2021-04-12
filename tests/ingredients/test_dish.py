import numpy as np
import pytest

from pyrogis.ingredients import Dish, Pierogi, Recipe


@pytest.fixture
def array():
    return np.asarray([[[200, 200, 200], [30, 30, 30]],
                       [[130, 130, 130], [60, 60, 60]]]).astype(np.dtype('uint8'))


@pytest.fixture
def image_file():
    return 'resources/gnome.jpg'


@pytest.fixture
def animation_file():
    return 'resources/octo.mp4'


def test_dish_pierogis_single(array):
    pierogi = Pierogi(pixels=array)

    dish = Dish(pierogi=pierogi)

    assert np.all(dish.pierogi.pixels == pierogi.pixels)


def test_dish_serve(array):
    pierogi = Pierogi(pixels=array)

    dish = Dish(pierogi=pierogi, recipe=Recipe())
    cooked_dish = dish.serve()

    assert np.all(cooked_dish.pierogi.pixels == pierogi.pixels)
