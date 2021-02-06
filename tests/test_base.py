import numpy as np
import pytest

from pyrogis import Base


@pytest.fixture
def array():
    return np.asarray([[[200, 200, 200], [30, 30, 30]],
                       [[130, 130, 130], [60, 60, 60]]])


def test_base_1(array):
    """
    test that a Pierogi can be created from an Image
    """

    pierogi = Base(pixels=array)

    assert np.all(pierogi.pixels[0, 0] == np.asarray([200, 200, 200]))
    assert np.all(pierogi.pixels[0, 1] == np.asarray([30, 30, 30]))
    assert np.all(pierogi.pixels[1, 0] == np.asarray([130, 130, 130]))
    assert np.all(pierogi.pixels[1, 1] == np.asarray([60, 60, 60]))
