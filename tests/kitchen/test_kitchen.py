import os

import pytest

from pierogis.kitchen import Order, Kitchen, Ticket


@pytest.fixture
def order(order_name: str, dir_path: str):
    order = Order(
        order_name,
        'input.mp4',
        fps=25,
        optimize=True
    )

    for filename in os.listdir(dir_path):
        if filename.startswith(order_name):
            order.add_ticket(
                Ticket(output_path=os.path.join(dir_path, filename)),
            )

    return order


def test_plate_gif(kitchen: Kitchen, order: Order, gif_output_path: str):
    order._output_path = gif_output_path

    output_path = kitchen.plate(
        order
    )

    assert os.path.isfile(output_path)


def test_plate_mp4(kitchen: Kitchen, order: Order, mp4_output_path: str):
    order._output_path = mp4_output_path

    output_path = kitchen.plate(
        order
    )

    assert os.path.isfile(output_path)


def test_plate_webm(kitchen: Kitchen, order: Order, webm_output_path: str):
    order._output_path = webm_output_path

    output_path = kitchen.plate(
        order
    )

    assert os.path.isfile(output_path)
