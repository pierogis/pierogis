import numpy as np
import pytest

from pyrogis import Dish, Pierogi


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

    dish = Dish(pierogis=[pierogi])

    assert np.all(dish.pierogis[0] == pierogi)


def test_dish_pierogis_multiple(array):
    pierogi = Pierogi(pixels=array)
    pierogi2 = Pierogi(pixels=np.rot90(array))

    dish = Dish(pierogis=[pierogi, pierogi2])

    assert np.all(dish.pierogis[1] == pierogi2)


def test_dish_from_path_image(image_file):
    dish = Dish.from_path(path=image_file)

    assert len(dish.pierogis) == 1


def test_dish_from_path_animation(animation_file):
    dish = Dish.from_path(path=animation_file)

    assert len(dish.pierogis) > 1
