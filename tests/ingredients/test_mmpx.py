import numpy as np
import pytest

from pierogis.ingredients import MMPX


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

    mmpx = MMPX()
    cooked_array = mmpx.cook(array)

    assert cooked_array.shape[0] == width * 2
    assert cooked_array.shape[1] == height * 2

    # it's just nearest neighbor for this input
    assert np.all(
        cooked_array == [
            [[200, 200, 200], [200, 200, 200], [30, 30, 30], [30, 30, 30]],
            [[200, 200, 200], [200, 200, 200], [30, 30, 30], [30, 30, 30]],
            [[130, 130, 130], [130, 130, 130], [60, 60, 60], [60, 60, 60]],
            [[130, 130, 130], [130, 130, 130], [60, 60, 60], [60, 60, 60]],
            [[20, 40, 100], [20, 40, 100], [10, 20, 200], [10, 20, 200]],
            [[20, 40, 100], [20, 40, 100], [10, 20, 200], [10, 20, 200]]
        ]
    )
