import numpy as np
import pytest

from pyrogis.ingredients.crop import Crop


@pytest.fixture
def array():
    return np.asarray([[[200, 200, 200], [30, 30, 30], [45, 90, 180]],
                       [[130, 130, 130], [60, 60, 60], [10, 90, 50]],
                       [[20, 40, 100], [10, 20, 200], [220, 25, 240]]]).astype(np.dtype('uint8'))


def test_crop_width(array):
    """
    provide only width
    """
    width = 1

    crop = Crop(width=width)
    cooked_array = crop.cook(array)

    assert cooked_array.shape[0] == width
    assert cooked_array.shape[1] == array.shape[1]


def test_crop_height(array):
    """
    provide only height
    """
    height = 2

    crop = Crop(height=height)
    cooked_array = crop.cook(array)

    assert cooked_array.shape[0] == array.shape[0]
    assert cooked_array.shape[1] == height


def test_crop_aspect_1(array):
    """
    provide only aspect with height limiting
    """
    aspect = 2 / 3

    crop = Crop(aspect=aspect)
    cooked_array = crop.cook(array)

    assert cooked_array.shape[0] == int(aspect * array.shape[0])
    assert cooked_array.shape[1] == array.shape[1]


def test_crop_aspect_2(array):
    """
    provide only aspect with width limiting
    """
    aspect = 3 / 2

    crop = Crop(aspect=aspect)
    cooked_array = crop.cook(array)

    assert cooked_array.shape[0] == array.shape[0]
    assert cooked_array.shape[1] == int(array.shape[1] / aspect)


def test_crop_width_height(array):
    """
    provide height and width
    """
    width = 2
    height = 1

    crop = Crop(width=width, height=height)
    cooked_array = crop.cook(array)

    assert cooked_array.shape[0] == width
    assert cooked_array.shape[1] == height


def test_crop_width_aspect(array):
    """
    provide width and aspect
    """
    width = 1
    aspect = 1 / 2

    crop = Crop(width=width, aspect=aspect)
    cooked_array = crop.cook(array)

    assert cooked_array.shape[0] == width
    assert cooked_array.shape[1] == width / aspect


def test_crop_height_aspect(array):
    """
    provide height and aspect
    """
    height = 1
    aspect = 2

    crop = Crop(aspect=aspect, height=height)
    cooked_array = crop.cook(array)

    assert cooked_array.shape[0] == height * aspect
    assert cooked_array.shape[1] == height


def test_crop_width_height_aspect(array):
    """
    provide width height and aspect

    just ignores aspect
    maybe it should fail
    """
    width = 2
    height = 1
    aspect = 2
    aspect = array.shape[0] / array.shape[1]

    crop = Crop(width=width, height=height, aspect=aspect)
    cooked_array = crop.cook(array)

    assert cooked_array.shape[0] == width
    assert cooked_array.shape[1] == height


def test_crop_x_y(array):
    """
    provide origin
    """
    x = 1
    y = 1

    crop = Crop(x=x, y=y)
    cooked_array = crop.cook(array)

    assert cooked_array.shape[0] == array.shape[0] - x
    assert cooked_array.shape[1] == array.shape[1] - y


def test_crop_x_y_height(array):
    """
    provide origin
    """
    x = 1
    y = 1
    height = 1

    crop = Crop(x=x, y=y, height=height)
    cooked_array = crop.cook(array)

    assert cooked_array.shape[0] == array.shape[0] - x
    assert cooked_array.shape[1] == height
