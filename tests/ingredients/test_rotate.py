import numpy as np
import pytest

from pyrogis.ingredients import Rotate


@pytest.fixture
def array():
    return np.asarray([[[200, 200, 200], [30, 30, 30]],
                       [[130, 130, 130], [60, 60, 60]],
                       [[20, 40, 100], [10, 20, 200]]]).astype(np.dtype('uint8'))


def test_cook(array):
    """
    provide only width
    """
    width, height = array.shape[:2]

    rotate = Rotate()
    cooked_array = rotate.cook(array)

    assert cooked_array.shape[0] == height
    assert cooked_array.shape[1] == width


def test_cook_angle(array):
    """
    provide only width
    """
    width, height = array.shape[:2]
    angle = 90

    rotate = Rotate(angle=angle)
    cooked_array = rotate.cook(array)

    assert cooked_array.shape[0] == height
    assert cooked_array.shape[1] == width


def test_cook_angle_turns_clockwise(array):
    """
    provide only width
    """
    width, height = array.shape[:2]
    angle = 90
    turns = 2
    clockwise = 2

    rotate = Rotate(angle=angle, turns=turns, clockwise=clockwise)
    cooked_array = rotate.cook(array)

    assert cooked_array.shape[0] == width
    assert cooked_array.shape[1] == height


def test_cook_angle_resample(array):
    """
    provide only width
    """
    width, height = array.shape[:2]
    angle = 20
    resample = 3

    rotate = Rotate(angle=angle, resample=resample)
    cooked_array = rotate.cook(array)

    assert cooked_array.shape[0] != width
    assert cooked_array.shape[1] != height
