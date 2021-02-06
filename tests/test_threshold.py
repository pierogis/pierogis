import numpy as np
import pytest

from pyrogis import Threshold


@pytest.fixture
def array():
    return np.asarray([[[200, 200, 200], [30, 30, 30]],
                       [[130, 130, 130], [60, 60, 60]]])


def test_threshold_1(array):
    """
    default
    """
    threshold = Threshold()

    cooked_array = threshold.cook(array)

    assert np.all(cooked_array[0, 0] == 255)
    assert np.all(cooked_array[0, 1] == 255)
    assert np.all(cooked_array[1, 0] == 0)
    assert np.all(cooked_array[1, 1] == 255)


def test_threshold_2(array):
    """
    upper threshold provided
    lower threshold should be 0
    """
    threshold = Threshold(
        upper_threshold=100
    )

    cooked_array = threshold.cook(array)

    assert np.all(cooked_array[0, 0] == 255)
    assert np.all(cooked_array[0, 1] == 0)
    assert np.all(cooked_array[1, 0] == 255)
    assert np.all(cooked_array[1, 1] == 0)


def test_threshold_3(array):
    """
    both thresholds provided
    """
    threshold = Threshold(
        upper_threshold=100,
        lower_threshold=40
    )

    cooked_array = threshold.cook(array)

    assert np.all(cooked_array[0, 0] == 255)
    assert np.all(cooked_array[0, 1] == 255)
    assert np.all(cooked_array[1, 0] == 255)
    assert np.all(cooked_array[1, 1] == 0)


def test_threshold_4(array):
    """
    using different pixels for replace
    """
    include_pixel = np.asarray([100, 100, 100])
    exclude_pixel = np.asarray([0, 0, 0])

    threshold = Threshold(
        include_pixel=include_pixel,
        exclude_pixel=exclude_pixel
    )

    cooked_array = threshold.cook(array)

    assert np.all(cooked_array[0, 0] == 100)
    assert np.all(cooked_array[0, 1] == 100)
    assert np.all(cooked_array[1, 0] == 0)
    assert np.all(cooked_array[1, 1] == 100)
