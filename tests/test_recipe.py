import numpy as np
import pytest

from pyrogis import Recipe, Ingredient
from pyrogis.ingredients import Rotate


@pytest.fixture
def array():
    return np.asarray([[[200, 200, 200], [30, 30, 30]],
                       [[130, 130, 130], [60, 60, 60]]]).astype(np.dtype('uint8'))


def test_recipe_1(array):
    recipe = Recipe()
    cooked_array = recipe.cook(array)

    assert np.all(array == cooked_array)
