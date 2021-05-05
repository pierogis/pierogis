import numpy as np
import pytest

from pierogis.ingredients import Recipe, Ingredient


@pytest.fixture
def array():
    return np.asarray([[[200, 200, 200], [30, 30, 30]],
                       [[130, 130, 130], [60, 60, 60]]]).astype(np.dtype('uint8'))

@pytest.fixture
def ingredient():
    return Ingredient()

def test_cook(array):
    recipe = Recipe()
    cooked_array = recipe.cook(array)

    assert np.all(array == cooked_array)

def test_add(ingredient):
    recipe = Recipe()
    cooked_array = recipe.add(ingredient)

    assert len(recipe.ingredients) == 1