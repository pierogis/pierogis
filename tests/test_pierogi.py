from io import BytesIO

import numpy as np
import pytest
from PIL import Image

from pyrogis import Pierogi


@pytest.fixture
def array():
    return np.asarray([[[200, 200, 200], [30, 30, 30]],
                       [[130, 130, 130], [60, 60, 60]]]).astype(np.dtype('uint8'))


@pytest.fixture
def file(array):
    image = Image.fromarray(array)
    output = image.tobytes()

    return 'imageio:chelsea.png'


def test_pierogi_1(array):
    """
    test that a Pierogi can be created from an Image
    """

    image = Image.fromarray(array)

    pierogi = Pierogi(image=image)

    assert np.all(pierogi.pixels[0, 0] == np.asarray([200, 200, 200]))
    assert np.all(pierogi.pixels[0, 1] == np.asarray([30, 30, 30]))
    assert np.all(pierogi.pixels[1, 0] == np.asarray([130, 130, 130]))
    assert np.all(pierogi.pixels[1, 1] == np.asarray([60, 60, 60]))


def test_pierogi_2(file):
    """
    test that a Pierogi can be created from a file
    """

    pierogi = Pierogi(file=file)

    assert np.all(pierogi.pixels[0, 0] == np.asarray([143, 120, 104]))
    assert np.all(pierogi.pixels[0, 1] == np.asarray([30, 30, 30]))
    assert np.all(pierogi.pixels[1, 0] == np.asarray([130, 130, 130]))
    assert np.all(pierogi.pixels[1, 1] == np.asarray([60, 60, 60]))
