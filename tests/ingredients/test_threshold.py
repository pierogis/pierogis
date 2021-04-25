import numpy as np
import pytest

from pyrogis.ingredients import Threshold


@pytest.fixture
def array():
    return np.asarray([[[200, 200, 200], [30, 30, 30]],
                       [[130, 130, 130], [60, 60, 60]]])


def test_cook(array):
    """default cook parameters"""
    threshold = Threshold()

    cooked_array = threshold.cook(array)

    assert np.all(cooked_array[0, 0] == 255)
    assert np.all(cooked_array[0, 1] == 255)
    assert np.all(cooked_array[1, 0] == 0)
    assert np.all(cooked_array[1, 1] == 255)


def test_cook_inner(array):
    """default cook parameters"""
    threshold = Threshold(inner=True)

    cooked_array = threshold.cook(array)

    assert np.all(cooked_array[0, 0] == 0)
    assert np.all(cooked_array[0, 1] == 0)
    assert np.all(cooked_array[1, 0] == 255)
    assert np.all(cooked_array[1, 1] == 255)


def test_cook_upper(array):
    """upper threshold provided; lower threshold should be 0"""
    threshold = Threshold(
        upper_threshold=100
    )

    assert threshold.lower_threshold == 0

    cooked_array = threshold.cook(array)

    assert np.all(cooked_array[0, 0] == 255)
    assert np.all(cooked_array[0, 1] == 0)
    assert np.all(cooked_array[1, 0] == 255)
    assert np.all(cooked_array[1, 1] == 0)


def test_cook_lower(array):
    """lower threshold provided; upper threshold should be 255"""
    threshold = Threshold(
        lower_threshold=100
    )

    assert threshold.upper_threshold == 255

    cooked_array = threshold.cook(array)

    assert np.all(cooked_array[0, 0] == 0)
    assert np.all(cooked_array[0, 1] == 255)
    assert np.all(cooked_array[1, 0] == 0)
    assert np.all(cooked_array[1, 1] == 255)


def test_cook_lower_upper(array):
    """both thresholds provided"""
    threshold = Threshold(
        upper_threshold=100,
        lower_threshold=40
    )

    cooked_array = threshold.cook(array)

    assert np.all(cooked_array[0, 0] == 255)
    assert np.all(cooked_array[0, 1] == 255)
    assert np.all(cooked_array[1, 0] == 255)
    assert np.all(cooked_array[1, 1] == 0)


def test_cook_include_exclude(array):
    """using different pixels for replace"""
    include_pixel = np.asarray([100, 100, 100])
    exclude_pixel = np.asarray([0, 0, 0])

    threshold = Threshold(
        include=include_pixel,
        exclude=exclude_pixel
    )

    cooked_array = threshold.cook(array)

    assert np.all(cooked_array[0, 0] == 100)
    assert np.all(cooked_array[0, 1] == 100)
    assert np.all(cooked_array[1, 0] == 0)
    assert np.all(cooked_array[1, 1] == 100)


def test_cook_np_rs(array):
    """test cook and cook_np method return the same array"""
    threshold = Threshold()

    rs_cooked_array = threshold.cook_rs(array)
    np_cooked_array = threshold.cook_np(array)

    assert np.all(rs_cooked_array == np_cooked_array)


def test_cook_np_rs_inner(array):
    """test cook and cook_np method return the same array"""
    threshold = Threshold(inner=True)

    rs_cooked_array = threshold.cook_rs(array)
    np_cooked_array = threshold.cook_np(array)

    assert np.all(rs_cooked_array == np_cooked_array)
