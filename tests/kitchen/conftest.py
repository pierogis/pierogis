import os

import imageio
import numpy as np
import pytest

from pyrogis.kitchen import Kitchen, Chef


@pytest.fixture
def array():
    return np.asarray([[[200, 200, 200], [30, 30, 30]],
                       [[130, 130, 130], [60, 60, 60]]]).astype(np.dtype('uint8'))


@pytest.fixture
def kitchen(tmp_path) -> Kitchen:
    return Kitchen(Chef, cooked_dir=str(tmp_path / 'cooked'), output_dir=str(tmp_path))


@pytest.fixture
def order_name():
    return 'octo'


@pytest.fixture
def image_path(array: np.ndarray, tmp_path):
    output_path = tmp_path / 'output.png'
    imageio.imwrite(output_path, array)

    return str(output_path)


@pytest.fixture
def animation_path(array, tmp_path) -> str:
    output_path = tmp_path / 'output.mp4'
    imageio.mimwrite(output_path, ims=[array, array])

    return str(output_path)


@pytest.fixture
def dir_path(image_path, tmp_path, order_name) -> str:
    frames_path = tmp_path / 'frames'
    im = imageio.imread(image_path)
    os.mkdir(frames_path)
    imageio.imwrite(frames_path / (order_name + '-1.png'), im=im)
    imageio.imwrite(frames_path / (order_name + '-2.png'), im=im)

    return str(frames_path)


@pytest.fixture
def png_output_path(tmp_path):
    return str(tmp_path / 'output.png')


@pytest.fixture
def gif_output_path(tmp_path):
    return str(tmp_path / 'output.gif')


@pytest.fixture
def mp4_output_path(tmp_path):
    return str(tmp_path / 'output.mp4')
