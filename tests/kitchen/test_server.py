import os
from typing import List

import pytest

from pyrogis.kitchen import Kitchen, Server, Ticket
from pyrogis.kitchen.menu import ResizeFilling
from pyrogis.kitchen.order import Order


@pytest.fixture
def server() -> Server:
    return Server()


@pytest.fixture
def parsed_vars() -> dict:
    parsed_vars = {
        'filling': 'resize',
        'generate_ticket': ResizeFilling.generate_ticket
    }
    return parsed_vars


@pytest.fixture
def image_order(order_name, image_path) -> Order:
    return Order(order_name, image_path)


@pytest.fixture
def animation_order(order_name, animation_path) -> Order:
    return Order(order_name, animation_path)


@pytest.fixture
def dir_order(order_name, dir_path) -> Order:
    return Order(order_name, dir_path)


@pytest.fixture
def recipe_path(tmp_path):
    recipe_text = """
    resize -s .5;
    sort;
    quantize;
    resize -s 2;
    """
    recipe_path = tmp_path / 'recipe.txt'
    with open(recipe_path, 'w') as f:
        f.write(recipe_text)

    return str(recipe_path)


def test_write_tickets_image(server: Server, image_order: Order, parsed_vars):
    server._write_tickets(image_order, parsed_vars)

    assert len(image_order.tickets) == 1


def test_write_tickets_animation(server, animation_order: Order, parsed_vars):
    server._write_tickets(animation_order, parsed_vars)

    assert len(animation_order.tickets) > 1


def test_check_cooked(server: Server, image_order: Order, image_path: str):
    image_order.tickets = [Ticket(output_path=image_path)]
    server.check_order(order=image_order)


# take_order

def run_take_order(server: Server, kitchen: Kitchen, args: List[str]):
    """

    """
    order = server.take_order(args, kitchen)

    for output_path in order.output_paths:
        assert os.path.isfile(output_path)


def test_take_order_sort(server, kitchen, image_path):
    args = ["sort", image_path]

    run_take_order(server, kitchen, args)


def test_take_order_sort_options(server, kitchen, image_path):
    """
    test sort order with options
    """
    args = ["sort", image_path, "-u", "120", "-l", "20", "-t", "2", "--ccw"]

    run_take_order(server, kitchen, args)


def test_take_order_quantize(server, kitchen, image_path):
    args = ["quantize", image_path]
    run_take_order(server, kitchen, args)


def test_take_order_quantize_options(server, kitchen, image_path):
    """
    test quantize order with options
    """
    args = [
        "quantize", image_path,
        "-c", "012312", "043251",
        "-n", "4",
        "--iterations", "2",
        "--repeats", "2",
        "--initial-temp", ".8",
        "--final-temp", "0.1",
        "--dithering-level", "0.5",
    ]

    run_take_order(server, kitchen, args)


def test_take_order_threshold(server, kitchen, image_path):
    args = ["threshold", image_path]

    run_take_order(server, kitchen, args)


def test_take_order_threshold_options(server, kitchen, image_path):
    """
    test threshold order with options
    """
    args = [
        "threshold", image_path,
        "-u", "200",
        "-l", "20",
        "-i", "abaabb",
        "-e", "333433"
    ]

    run_take_order(server, kitchen, args)


def test_take_order(server, kitchen, image_path):
    args = ["resize", image_path]

    run_take_order(server, kitchen, args)


def test_take_order_resize_options(server, kitchen, image_path):
    """
    test resize order with options
    """
    args = [
        "resize", image_path,
        "--width", "200",
        "--height", "300",
        "-s", "2",
        "-r", "bicubic"
    ]

    run_take_order(server, kitchen, args)


def test_take_order_chef(server, kitchen, image_path):
    args = ["custom", image_path, "sort; quantize"]

    run_take_order(server, kitchen, args)


def test_take_order_chef_txt(server, kitchen, image_path, recipe_path):
    args = ["custom", image_path, recipe_path]

    run_take_order(server, kitchen, args)


def test_take_order_togo(server, kitchen, dir_path):
    args = ["togo", dir_path]

    run_take_order(server, kitchen, args)


def test_take_order_togo_options(server, kitchen, dir_path, mp4_output_path):
    args = [
        "togo", dir_path,
        "--fps", "25",
        "--frame-duration", "20",
        "--no-optimize",
        "--output", mp4_output_path,
        "--order-name", "octo"
    ]

    run_take_order(server, kitchen, args)


# def test_take_order_image_with_output():
#     args=["resize", image_path, "--output", "output.png"]
#
#     order_name = 'resize'
#
#     take_order(args, order_name)


def test_take_order_animation(server, kitchen, animation_path):
    """
    test making an animation order
    """
    args = ["resize", animation_path]

    run_take_order(server, kitchen, args)

# def test_take_order_animation_with_output_gif():
#     """
#     test making an animation order
#     and providing an output gif filename
#     """
#     args=["resize", "resources/octo.mp4", "--output", "output.gif"]
#     order_name = 'resize'
#
#     take_order(args, order_name)
#
# def test_take_order_animation_with_output_mp4():
#     """
#     test making an animation order
#     and providing an output gif filename
#     """
#     args=["resize", "resources/octo.mp4", "--output", "cooked.mp4"]
#     order_name = 'resize'
#
#     take_order(args, order_name)


# def test_take_order_animation_frames():
#     """
#     test making an animation order and not bundling the output
#     """
#     args=["resize", "resources/octo.mp4", "--frames"]
#
#     order_name = 'resize'
#
#     take_order(args, order_name)
#
#
# def test_take_order_animation_frames_with_output_dir():
#     """
#     test making an animation order and not bundling the output
#     provided an output dir
#     """
#     args=["resize", "resources/octo.mp4", "--frames", "--output", "frames"]
#     order_name = 'quantize'
#
#     take_order(args, order_name)
