import os
import time
from typing import List

import pytest

from pyrogis import Dish, Pierogi
from pyrogis.kitchen import Kitchen, Chef, Server, Ticket
from pyrogis.kitchen.menu import ResizeFilling
from pyrogis.kitchen.order import Order


@pytest.fixture
def resource_dir(request) -> str:
    return os.path.join(request.config.rootdir, 'tests', 'resources')


@pytest.fixture
def server() -> Server:
    return Server()


@pytest.fixture
def image_path(resource_dir) -> str:
    return os.path.join(resource_dir, 'gnome.jpg')


@pytest.fixture
def animation_path(resource_dir) -> str:
    return os.path.join(resource_dir, 'octo.mp4')


@pytest.fixture
def dir_path(resource_dir) -> str:
    return os.path.join(resource_dir, 'frames')


@pytest.fixture
def image_dish(image_path) -> Dish:
    return Dish(pierogi=Pierogi.from_path(image_path))


@pytest.fixture
def animation_dish(animation_path) -> Dish:
    return Dish(pierogi=Pierogi.from_path(animation_path))


@pytest.fixture
def parsed_vars() -> dict:
    parsed_vars = {
        'order': 'resize',
        'generate_ticket': ResizeFilling.generate_ticket
    }
    return parsed_vars


@pytest.fixture
def image_args(image_path) -> List[str]:
    args = ['resize', image_path]

    return args


@pytest.fixture
def animation_args(animation_path) -> List[str]:
    args = ['resize', animation_path]

    return args


@pytest.fixture
def dir_args(dir_path) -> List[str]:
    args = ['resize', dir_path]

    return args


@pytest.fixture
def kitchen() -> Kitchen:
    return Kitchen(Chef)


@pytest.fixture
def image_order(image_path) -> Order:
    return Order('image', image_path)


@pytest.fixture
def animation_order(animation_path) -> Order:
    return Order('animation', animation_path)


@pytest.fixture
def dir_order(dir_path) -> Order:
    return Order('octo', dir_path)


def test_write_tickets_image(server: Server, image_order: Order, parsed_vars):
    server.write_tickets(image_order, parsed_vars)

    assert len(image_order.tickets) == 1


def test_write_tickets_animation(server, animation_order: Order, parsed_vars):
    server.write_tickets(animation_order, parsed_vars)

    assert len(animation_order.tickets) > 1


def test_check_cooked(server: Server, image_order: Order, image_path: str):
    image_order.tickets = [Ticket(output_filename=image_path)]
    server.check_order(order=image_order)


# take_order

def run_take_order(server: Server, kitchen: Kitchen, args: List[str], wait: float = .1):
    """

    """
    server.take_order(args, kitchen)

    time.sleep(wait)

    for output_filename in output_filenames:
        assert os.path.isfile(output_filename)
        os.remove(output_filename)


def test_take_order_sort(server, kitchen, image_path):
    args = ["sort", image_path]

    run_take_order(server, kitchen, args)


def test_take_order_sort_options(server, kitchen, image_path):
    """
    test sort order with options
    """
    args = ["sort", image_path, "-u", "120", "-l", "20", "-t", "2", "--ccw"]

    run_take_order(server, kitchen, args)


def test_take_order_quantize(server, kitchen):
    args = ["quantize", "resources/gnome.jpg"]
    run_take_order(server, kitchen, args)


def test_take_order_quantize_options(server, kitchen):
    """
    test quantize order with options
    """
    args = [
        "quantize", "resources/gnome.jpg",
        "-c", "012312", "043251",
        "-n", "4",
        "--iterations", "2",
        "--repeats", "2",
        "--initial-temp", ".8",
        "--final-temp", "0.1",
        "--dithering-level", "0.5",
    ]

    run_take_order(server, kitchen, args)


def test_take_order_threshold(server, kitchen):
    args = ["threshold", "resources/gnome.jpg"]

    run_take_order(server, kitchen, args)


def test_take_order_threshold_options(server, kitchen):
    """
    test threshold order with options
    """
    args = [
        "threshold", "resources/gnome.jpg",
        "-u", "200",
        "-l", "20",
        "-i", "abaabb",
        "-e", "333433"
    ]

    run_take_order(server, kitchen, args)


def test_take_order(server, kitchen):
    args = ["resize", "resources/gnome.jpg"]

    run_take_order(server, kitchen, args)


def test_take_order_resize_options(server, kitchen):
    """
    test resize order with options
    """
    args = [
        "resize", "resources/gnome.jpg",
        "--width", "200",
        "--height", "300",
        "-s", "2",
        "-r", "bicubic"
    ]

    run_take_order(server, kitchen, args)


def test_take_order_chef(server, kitchen):
    args = ["chef", "resources/gnome.jpg", "sort; quantize"]

    run_take_order(server, kitchen, args)


def test_take_order_chef_txt(server, kitchen):
    args = ["chef", "resources/gnome.jpg", "resources/recipe.txt"]

    run_take_order(server, kitchen, args)


def test_take_order_togo(server, kitchen):
    args = ["togo", "resources/frames"]

    run_take_order(server, kitchen, args)


def test_take_order_togo_options(server, kitchen):
    args = [
        "togo", "resources/frames",
        "--fps", "25",
        "--frame-duration", "20",
        "--no-optimize",
        "--output", "frames.mp4",
        "--order-name", "octo"
    ]

    run_take_order(server, kitchen, args)


# def test_take_order_image_with_output():
#     args=["resize", "resources/gnome.jpg", "--output", "output.png"]
#
#     order_name = 'resize'
#
#     take_order(args, order_name)


def test_take_order_animation(server, kitchen):
    """
    test making an animation order
    """
    args = ["resize", "resources/octo.mp4"]

    run_take_order(server, kitchen, args, 1)

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
