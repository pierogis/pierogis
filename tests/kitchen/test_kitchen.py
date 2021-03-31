import os

import pytest

from pyrogis.kitchen import Order, Kitchen, Chef, Ticket


@pytest.fixture
def resource_dir(request) -> str:
    return os.path.join(request.config.rootdir, 'tests', 'resources')


@pytest.fixture
def kitchen() -> Kitchen:
    return Kitchen(Chef())


def test_plate_gif(kitchen: Kitchen, resource_dir: str, tmp_path):
    input_path = os.path.join(resource_dir, 'octo.gif')
    output_path = tmp_path / 'output.gif'
    optimize = True

    order = Order(
        'octo',
        input_path,
        output_path=output_path,
        fps=25,
        optimize=optimize
    )

    order.tickets = [
        Ticket(),
        Ticket()
    ]

    output_path = kitchen.plate(
        order
    )

    assert os.path.isfile(output_path)


def test_plate_mp4(kitchen: Kitchen, resource_dir: str, tmp_path):
    input_path = os.path.join(resource_dir, 'octo.mp4')
    output_path = tmp_path / 'output.mp4'
    optimize = True

    order = Order(
        'octo',
        input_path,
        output_path=output_path,
        fps=25,
        optimize=optimize
    )

    order.tickets = [
        Ticket(),
        Ticket()
    ]

    output_path = kitchen.plate(
        order
    )

    assert os.path.isfile(output_path)


def test_plate_dir(kitchen: Kitchen, resource_dir: str, tmp_path):
    input_path = os.path.join(resource_dir, 'frames')
    output_path = tmp_path / 'output.mp4'
    optimize = True

    order = Order(
        'octo',
        input_path,
        output_path=output_path,
        fps=25,
        optimize=optimize
    )

    order.tickets = [
        Ticket(output_filename=os.path.join(input_path, 'octo-01.png')),
        Ticket(output_filename=os.path.join(input_path, 'octo-02.png'))
    ]

    kitchen.plate(order)

    assert os.path.isfile(output_path)
