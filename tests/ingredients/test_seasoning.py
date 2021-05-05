import numpy as np
import pytest

from pierogis.ingredients.seasonings import Seasoning


@pytest.fixture
def array():
    return np.asarray([[[0, 0, 0], [255, 255, 255]],
                       [[130, 130, 130], [60, 60, 60]]])


def test_cook(array: np.ndarray):
    seasoning = Seasoning()
    cooked_array = seasoning.cook(array)

    assert np.all(cooked_array[0, 1] == 255)
