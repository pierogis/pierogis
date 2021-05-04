import os
from io import BytesIO

import numpy as np
import pytest
from PIL import Image

from pierogis.ingredients import Pierogi


@pytest.fixture
def array():
    return np.asarray([[[200, 200, 200], [30, 30, 30]],
                       [[130, 130, 130], [60, 60, 60]]]).astype(np.dtype('uint8'))


@pytest.fixture
def file(array: np.ndarray):
    image = Image.fromarray(array)
    memory = BytesIO()
    image.save(memory, format="PNG")

    return memory


@pytest.fixture
def path(array: np.ndarray, tmp_path):
    image = Image.fromarray(array)
    output_path = tmp_path / 'output.png'
    image.save(output_path)

    return output_path


def test_from_pil_image(file: BytesIO):
    """
    test that a Pierogi can be created from an Image
    """
    image = Image.open(file)
    pierogi = Pierogi.from_pil_image(image=image)

    assert np.all(pierogi.pixels[0, 0] == np.asarray([130, 130, 130]))
    assert np.all(pierogi.pixels[0, -1] == np.asarray([200, 200, 200]))
    assert np.all(pierogi.pixels[-1, 0] == np.asarray([60, 60, 60]))
    assert np.all(pierogi.pixels[-1, -1] == np.asarray([30, 30, 30]))


def test_from_path(path: str):
    """
    test that a Pierogi can be created from a file
    """

    pierogi = Pierogi.from_path(path=path)

    assert np.all(pierogi.pixels[0, 0] == np.asarray([130, 130, 130]))
    assert np.all(pierogi.pixels[0, -1] == np.asarray([200, 200, 200]))
    assert np.all(pierogi.pixels[-1, 0] == np.asarray([60, 60, 60]))
    assert np.all(pierogi.pixels[-1, -1] == np.asarray([30, 30, 30]))


def test_save(array: np.ndarray, tmp_path):
    """
    test resample can be used
    """

    pierogi = Pierogi(pixels=array)

    path = tmp_path / "output.png"
    pierogi.save(path)

    assert os.path.exists(path)


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
