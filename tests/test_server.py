import os
import time
from typing import List

import pytest

from pyrogis import Dish
from pyrogis.kitchen import Kitchen, Chef, Server
from pyrogis.kitchen.menu import ResizeOrder


@pytest.fixture
def server() -> Server:
    return Server()


@pytest.fixture
def image_file() -> str:
    return 'resources/gnome.jpg'


@pytest.fixture
def image_dish(image_file) -> Dish:
    return Dish.from_path(image_file)


@pytest.fixture
def animation_file() -> str:
    return 'resources/octo.mp4'


@pytest.fixture
def animation_dish(animation_file) -> Dish:
    return Dish.from_path(animation_file)


@pytest.fixture
def parsed_vars() -> dict:
    parsed_vars = {
        'order': 'resize',
        'generate_ticket': ResizeOrder.generate_ticket
    }
    return parsed_vars


@pytest.fixture
def image_args() -> List[str]:
    args = ['resize', 'resources/gnome.jpg']

    return args


@pytest.fixture
def animation_args() -> List[str]:
    args = ['resize', 'resources/octo.mp4']

    return args


@pytest.fixture
def dir_args() -> List[str]:
    args = ['resize', 'resources/frames']

    return args


@pytest.fixture
def kitchen():
    return Kitchen(Chef())


def test_write_tickets_image(server: Server, image_file, image_dish: Dish, parsed_vars):
    order_name = 'test_server_write_tickets_image'

    tickets = list(server.write_tickets(order_name, image_dish, image_file, parsed_vars))

    assert len(tickets) == 1


def test_write_tickets_animation(server, animation_file, animation_dish, parsed_vars):
    order_name = 'test_server_write_tickets_animation'

    tickets = list(server.write_tickets(animation_dish, animation_file, parsed_vars))

    assert len(tickets) > 1


def test_togo_gif(server):
    order_name = 'test_togo_gif'
    input_path = 'resources/octo.mp4'
    output_filename = 'output.gif'
    optimize = True
    dish = Dish.from_path(path=input_path)
    output_path = server.togo(
        dish,
        order_name,
        output_filename=output_filename,
        fps=25,
        optimize=optimize
    )

    assert os.path.isfile(output_path)

    os.remove(output_path)


def test_togo_mp4(server):
    order_name = 'test_togo_gif'
    input_path = 'resources/octo.mp4'
    output_filename = 'output.mp4'
    optimize = True
    dish = Dish.from_path(path=input_path)
    output_path = server.togo(
        dish,
        order_name,
        output_filename=output_filename,
        fps=25,
        optimize=optimize
    )

    assert os.path.isfile(output_path)

    os.remove(output_path)


def test_togo_dir(server):
    order_name = 'test_togo_dir'
    input_path = 'resources/frames'
    output_filename = 'output.mp4'
    optimize = True
    output_path = server.togo(
        input_path=input_path,
        order_name=order_name,
        output_filename=output_filename,
        fps=25,
        optimize=optimize
    )

    assert os.path.isfile(output_path)

    os.remove(output_path)


def test_check_cooked(server):
    order_name = 'test_check_cooked'

    assert server.check_order(order_name=order_name)


# take_order

def take_order(server, kitchen, args, order_name):
    output_filenames = server.take_order(args, kitchen, order_name)

    time.sleep(2)

    for output_filename in output_filenames:
        assert os.path.isfile(output_filename)
        os.remove(output_filename)


def test_take_order_sort(server, kitchen):
    args = ["sort", "resources/gnome.jpg"]

    order_name = 'sort'

    take_order(server, kitchen, args, order_name)


def test_take_order_sort_options(server, kitchen):
    """
    test sort order with options
    """
    args = ["sort", "resources/gnome.jpg", "-u", "120", "-l", "20", "-t", "2", "--ccw"]

    order_name = 'sort'

    take_order(server, kitchen, args, order_name)


def test_take_order_quantize(server, kitchen):
    args = ["quantize", "resources/gnome.jpg"]

    order_name = 'quantize'

    take_order(server, kitchen, args, order_name)


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

    order_name = 'quantize'

    take_order(server, kitchen, args, order_name)


def test_take_order_threshold(server, kitchen):
    args = ["threshold", "resources/gnome.jpg"]

    order_name = 'threshold'

    take_order(server, kitchen, args, order_name)


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

    order_name = 'threshold'

    take_order(server, kitchen, args, order_name)


def test_take_order_resize(server, kitchen):
    args = ["resize", "resources/gnome.jpg"]

    order_name = 'resize'

    take_order(server, kitchen, args, order_name)


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

    order_name = 'resize'

    take_order(server, kitchen, args, order_name)


def test_take_order_chef(server, kitchen):
    args = ["chef", "resources/gnome.jpg", "sort; quantize"]

    order_name = 'chef'

    take_order(server, kitchen, args, order_name)


def test_take_order_chef_txt(server, kitchen):
    args = ["chef", "resources/gnome.jpg", "resources/recipe.txt"]

    order_name = 'chef'

    take_order(args, order_name)


def test_take_order_plate():
    args = ["togo", "resources/frames"]

    order_name = 'togo'

    take_order(args, order_name)


def test_take_order_plate_options():
    args = ["togo", "resources", "--fps", "25", "--duration", "20", "--no-optimize"]

    order_name = 'togo'

    take_order(args, order_name)


# def test_take_order_image_with_output():
#     args=["resize", "resources/gnome.jpg", "--output", "output.png"]
#
#     order_name = 'resize'
#
#     take_order(args, order_name)


def test_take_order_animation():
    """
    test making an animation order
    """
    args = ["resize", "resources/octo.mp4"]
    order_name = 'resize'

    take_order(args, order_name)

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
