import numpy as np
import pytest
from PIL import Image

from pyrogis import Pierogi


@pytest.fixture
def array():
    return np.asarray([[[200, 200, 200], [30, 30, 30]],
                       [[130, 130, 130], [60, 60, 60]]]).astype(np.dtype('uint8'))


@pytest.fixture
def file(array: np.ndarray):
    image = Image.fromarray(array)
    output = image.tobytes()

    return 'resources/gnome.jpg'


def test_from_pil_image(file: str):
    """
    test that a Pierogi can be created from an Image
    """
    image = Image.open(file)
    pierogi = Pierogi.from_pil_image(image=image)

    assert np.all(pierogi.pixels[0, 0] == np.asarray([137, 139, 115]))
    assert np.all(pierogi.pixels[0, -1] == np.asarray([59, 59, 67]))
    assert np.all(pierogi.pixels[-1, 0] == np.asarray([144, 176, 127]))
    assert np.all(pierogi.pixels[-1, -1] == np.asarray([90, 81, 66]))


def test_from_path(file: str):
    """
    test that a Pierogi can be created from a file
    """

    pierogi = Pierogi.from_path(path=file)

    assert np.all(pierogi.pixels[0, 0] == np.asarray([137, 139, 115]))
    assert np.all(pierogi.pixels[0, -1] == np.asarray([59, 59, 67]))
    assert np.all(pierogi.pixels[-1, 0] == np.asarray([144, 176, 127]))
    assert np.all(pierogi.pixels[-1, -1] == np.asarray([90, 81, 66]))


def test_resize(array: np.ndarray):
    """
    test resize method
    """

    pierogi = Pierogi(pixels=array)

    width = 100
    height = 200

    pierogi.resize(width=width, height=height)

    assert pierogi.width == width
    assert pierogi.height == height

    # nearest neighbor default
    assert np.all(pierogi.pixels[0, 0] == array[0, 0])
    assert np.all(pierogi.pixels[0, -1] == array[0, -1])
    assert np.all(pierogi.pixels[-1, 0] == array[-1, 0])
    assert np.all(pierogi.pixels[-1, -1] == array[-1, -1])


def test_resize_resample(array: np.ndarray):
    """
    test resample can be used
    """

    pierogi = Pierogi(pixels=array)

    width = 100
    height = 200

    pierogi.resize(width=width, height=height, resample=Image.BICUBIC)

    assert pierogi.width == width
    assert pierogi.height == height
