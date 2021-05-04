import os
from typing import List

import pytest

from pierogis.kitchen import Kitchen, Server, Ticket
from pierogis.kitchen.menu import ResizeFilling
from pierogis.kitchen.order import Order


@pytest.fixture
def server(tmp_path) -> Server:
    return Server(output_dir=str(tmp_path))


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
    server._check_order(order=image_order)


# take_order

def run_take_order(
        server: Server, kitchen: Kitchen, args: List[str]
) -> Order:
    """handle take order call and successful output checking"""
    order = server.take_order(args, kitchen)

    for output_path in order.ticket_output_paths:
        assert os.path.isfile(output_path)

    return order


def test_take_order_sort(server, kitchen, image_path):
    """test sort order"""
    args = ["sort", image_path]

    run_take_order(server, kitchen, args)


def test_take_order_sort_options(server, kitchen, image_path):
    """test sort order with options"""
    args = [
        "sort", image_path,
        "-u", "120", "-l", "20",
        "--inner",
        "-t", "2", "--ccw"
    ]

    run_take_order(server, kitchen, args)


def test_take_order_quantize(server, kitchen, image_path):
    """test quantize order"""
    args = ["quantize", image_path]
    run_take_order(server, kitchen, args)


def test_take_order_quantize_options(server, kitchen, image_path):
    """test quantize order with options"""
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
    """test threshold order with options"""
    args = [
        "threshold", image_path,
        "-u", "200",
        "-l", "20",
        "--inner",
        "--include", "abaabb",
        "--exclude", "333433"
    ]

    run_take_order(server, kitchen, args)


def test_take_order_resize(server, kitchen, image_path):
    """test resize order"""
    args = ["resize", image_path]

    order = run_take_order(server, kitchen, args)

    assert len(order.tickets) == 1
    print(order.tickets[0].output_path)


def test_take_order_resize_options(server, kitchen, image_path):
    """test resize order with options"""
    args = [
        "resize", image_path,
        "--width", "200",
        "--height", "300",
        "-s", "2",
        "--resample-filter", "bicubic",
        "--presave",
        "--async",
        "--processes", "4"
    ]

    order = run_take_order(server, kitchen, args)

    assert order.processes == 4
    assert order.cook_async
    assert order.presave


def test_take_order_presave_async_processes(server, kitchen, image_path):
    """test queue/async options"""
    args = [
        "resize", image_path,
        "--presave",
        "--async",
        "--processes", "4"
    ]

    run_take_order(server, kitchen, args)


def test_take_order_resume(server, kitchen, animation_path):
    """test resume flag"""
    args = [
        "resize", animation_path,
        "--resume"
    ]

    run_take_order(server, kitchen, args)


def test_take_order_custom(server, kitchen, image_path):
    """test custom with a txt file as a recipe"""
    args = ["custom", image_path, "sort; quantize"]

    run_take_order(server, kitchen, args)


def test_take_order_custom_txt(server, kitchen, image_path, recipe_path):
    """test custom with a txt file as a recipe"""
    args = ["custom", image_path, recipe_path]

    run_take_order(server, kitchen, args)


def test_take_order_crop(server, kitchen, image_path, recipe_path):
    """test custom with a txt file as a recipe"""
    args = [
        "crop", image_path,
        "--width", "1",
        "--height", "1",
    ]

    run_take_order(server, kitchen, args)


def test_take_order_crop_options(server, kitchen, image_path, recipe_path):
    """test custom with a txt file as a recipe"""
    args = [
        "crop", image_path,
        "--origin", "ne",
        "--width", "1",
        "--height", "1",
    ]

    run_take_order(server, kitchen, args)


def test_take_order_crop_options_float(server, kitchen, image_path, recipe_path):
    """test custom with a txt file as a recipe"""
    args = [
        "crop", image_path,
        "--origin", "ne",
        "--width", "1",
        "--height", "1",
        "-x", "-0.5",
        "--aspect", "0.5",
    ]

    run_take_order(server, kitchen, args)


# non filling-related take_order tests
def test_take_order_togo(server, kitchen, dir_path):
    """test togo"""
    args = ["togo", dir_path]

    run_take_order(server, kitchen, args)


def test_take_order_togo_options(server, kitchen, dir_path, mp4_output_path):
    """test togo with options"""
    args = [
        "togo", dir_path,
        "--fps", "25",
        "--frame-duration", "20",
        "--no-optimize",
        "--output", mp4_output_path,
        "--order-name", "octo"
    ]

    run_take_order(server, kitchen, args)


def test_take_order_image_with_output(server, kitchen, image_path, png_output_path):
    """test image output path given"""
    args = ["resize", image_path, "--output", png_output_path]

    run_take_order(server, kitchen, args)


def test_take_order_animation(server, kitchen, animation_path):
    """test making an animation order"""
    args = ["resize", animation_path]

    run_take_order(server, kitchen, args)
