import os
from typing import List

import pytest

from pyrogis import Dish
from pyrogis.kitchen import Server, menu
from pyrogis.kitchen.menu import ResizeOrder


@pytest.fixture
def server() -> Server:
    return Server()


@pytest.fixture
def image_dish() -> Dish:
    return Dish.from_path('resources/gnome.jpg')


@pytest.fixture
def animation_dish() -> Dish:
    return Dish.from_path('resources/octo.mp4')


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


def test_write_tickets_image(server, image_dish, parsed_vars):
    order_name = 'test_server_write_tickets_image'

    tickets = server.write_tickets(order_name, image_dish, parsed_vars)

    assert len(tickets) == 1

    server.remove_order_dir(order_name)


def test_write_tickets_animation(server, animation_dish, parsed_vars):
    order_name = 'test_server_write_tickets_animation'

    tickets = server.write_tickets(order_name, animation_dish, parsed_vars)

    assert len(tickets) > 1

    server.remove_order_dir(order_name)


def test_take_orders_image(server, image_args):
    order_name = 'test_server_take_orders_image'
    tickets = server.take_orders(order_name, image_args, menu)

    assert len(tickets) == 1

    server.remove_order_dir(order_name)


def test_take_orders_animation(server, animation_args):
    order_name = 'test_server_take_orders_animation'
    tickets = server.take_orders(order_name, animation_args, menu)

    assert len(tickets) > 1

    server.remove_order_dir(order_name)


def test_take_orders_dir(server, dir_args):
    order_name = 'test_take_orders_dir'
    tickets = server.take_orders(order_name, dir_args, menu)

    assert len(tickets) > 1

    server.remove_order_dir(order_name)


def test_togo_gif(server):
    order_name = 'test_togo_gif'
    input_path = 'resources/octo.mp4'
    output_filename = 'output.gif'
    optimize = True
    dish = Dish.from_path(path=input_path)
    output_path = server.togo(order_name, dish, output_filename, 25, optimize)

    assert os.path.isfile(output_path)

    os.remove(output_path)


def test_togo_mp4(server):
    order_name = 'test_togo_gif'
    input_path = 'resources/octo.mp4'
    output_filename = 'output.mp4'
    optimize = True
    dish = Dish.from_path(path=input_path)
    output_path = server.togo(order_name, dish, output_filename, 25, optimize)

    assert os.path.isfile(output_path)

    os.remove(output_path)


def test_togo_dir(server):
    order_name = 'test_togo_dir'
    input_path = 'resources/frames'
    output_filename = 'output.mp4'
    optimize = True
    dish = Dish.from_path(path=input_path)
    output_path = server.togo(order_name, dish, output_filename, 25, optimize)

    assert os.path.isfile(output_path)

    os.remove(output_path)


def test_check(server):
    input_path = 'resources/frames'

    assert server.check(input_path) == 10
