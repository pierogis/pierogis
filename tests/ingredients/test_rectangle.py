import numpy as np
import pytest

from pyrogis.ingredients.seasonings import Rectangle
from pyrogis.ingredients.seasonings.rectangle import Direction


@pytest.fixture
def array():
    return np.zeros((500, 500, 3))


def test_get_corner_coordinates(array: np.ndarray):
    rectangle = Rectangle()
    bottom_left, top_right = rectangle.get_corner_coordinates(array.shape[0], array.shape[1])

    assert bottom_left.x == 0
    assert bottom_left.y == 0
    assert top_right.x == 500
    assert top_right.y == 500


def test_get_corner_coordinates_width_height_sw(array: np.ndarray):
    origin = Direction.SW
    width = 100
    height = 100

    rectangle = Rectangle(origin=origin, width=width, height=height)
    bottom_left, top_right = rectangle.get_corner_coordinates(array.shape[0], array.shape[1])

    assert bottom_left.x == 0
    assert bottom_left.y == 0
    assert top_right.x == 100
    assert top_right.y == 100


def test_get_corner_coordinates_width_height_se(array: np.ndarray):
    origin = Direction.SE
    width = 100
    height = 100

    rectangle = Rectangle(origin=origin, width=width, height=height)
    bottom_left, top_right = rectangle.get_corner_coordinates(array.shape[0], array.shape[1])

    assert bottom_left.x == 400
    assert bottom_left.y == 0
    assert top_right.x == 500
    assert top_right.y == 100


def test_get_corner_coordinates_width_height_nw(array: np.ndarray):
    origin = Direction.NW
    width = 100
    height = 100

    rectangle = Rectangle(origin=origin, width=width, height=height)
    bottom_left, top_right = rectangle.get_corner_coordinates(array.shape[0], array.shape[1])

    assert bottom_left.x == 0
    assert bottom_left.y == 400
    assert top_right.x == 100
    assert top_right.y == 500


def test_get_corner_coordinates_width_height_ne(array: np.ndarray):
    origin = Direction.NE
    width = 100
    height = 100

    rectangle = Rectangle(origin=origin, width=width, height=height)
    bottom_left, top_right = rectangle.get_corner_coordinates(array.shape[0], array.shape[1])

    assert bottom_left.x == 400
    assert bottom_left.y == 400
    assert top_right.x == 500
    assert top_right.y == 500


def test_get_corner_coordinates_width_height_c(array: np.ndarray):
    origin = Direction.C
    width = 100
    height = 100

    rectangle = Rectangle(origin=origin, width=width, height=height)
    bottom_left, top_right = rectangle.get_corner_coordinates(array.shape[0], array.shape[1])

    assert bottom_left.x == 200
    assert bottom_left.y == 200
    assert top_right.x == 300
    assert top_right.y == 300


def test_get_corner_coordinates_width_height_n(array: np.ndarray):
    origin = Direction.N
    width = 100
    height = 100

    rectangle = Rectangle(origin=origin, width=width, height=height)
    bottom_left, top_right = rectangle.get_corner_coordinates(array.shape[0], array.shape[1])

    assert bottom_left.x == 200
    assert bottom_left.y == 400
    assert top_right.x == 300
    assert top_right.y == 500


def test_get_corner_coordinates_width_height_e(array: np.ndarray):
    origin = Direction.E
    width = 100
    height = 100

    rectangle = Rectangle(origin=origin, width=width, height=height)
    bottom_left, top_right = rectangle.get_corner_coordinates(array.shape[0], array.shape[1])

    assert bottom_left.x == 400
    assert bottom_left.y == 200
    assert top_right.x == 500
    assert top_right.y == 300


def test_get_corner_coordinates_width_height_s(array: np.ndarray):
    origin = Direction.S
    width = 100
    height = 100

    rectangle = Rectangle(origin=origin, width=width, height=height)
    bottom_left, top_right = rectangle.get_corner_coordinates(array.shape[0], array.shape[1])

    assert bottom_left.x == 200
    assert bottom_left.y == 0
    assert top_right.x == 300
    assert top_right.y == 100


def test_get_corner_coordinates_width_height_w(array: np.ndarray):
    origin = Direction.W
    width = 100
    height = 100

    rectangle = Rectangle(origin=origin, width=width, height=height)
    bottom_left, top_right = rectangle.get_corner_coordinates(array.shape[0], array.shape[1])

    assert bottom_left.x == 0
    assert bottom_left.y == 200
    assert top_right.x == 100
    assert top_right.y == 300


def test_get_corner_coordinates_width_sw(array: np.ndarray):
    origin = Direction.SW
    width = 100

    rectangle = Rectangle(origin=origin, width=width)
    bottom_left, top_right = rectangle.get_corner_coordinates(array.shape[0], array.shape[1])

    assert bottom_left.x == 0
    assert bottom_left.y == 0
    assert top_right.x == 100
    assert top_right.y == 500


def test_get_corner_coordinates_height_sw(array: np.ndarray):
    origin = Direction.SW
    height = 100

    rectangle = Rectangle(origin=origin, height=height)
    bottom_left, top_right = rectangle.get_corner_coordinates(array.shape[0], array.shape[1])

    assert bottom_left.x == 0
    assert bottom_left.y == 0
    assert top_right.x == 500
    assert top_right.y == 100


def test_get_corner_coordinates_width_sw_x(array: np.ndarray):
    origin = Direction.SW
    x = 100
    width = 100

    rectangle = Rectangle(origin=origin, width=width, x=x)
    bottom_left, top_right = rectangle.get_corner_coordinates(array.shape[0], array.shape[1])

    assert bottom_left.x == 100
    assert bottom_left.y == 0
    assert top_right.x == 200
    assert top_right.y == 500


def test_get_corner_coordinates_width_sw_y(array: np.ndarray):
    origin = Direction.SW
    y = 100
    width = 100

    rectangle = Rectangle(origin=origin, width=width, y=y)
    bottom_left, top_right = rectangle.get_corner_coordinates(array.shape[0], array.shape[1])

    assert bottom_left.x == 0
    assert bottom_left.y == 100
    assert top_right.x == 100
    assert top_right.y == 500


def test_get_corner_coordinates_width_nw_x(array: np.ndarray):
    origin = Direction.NW
    x = 100
    width = 100

    rectangle = Rectangle(origin=origin, width=width, x=x)
    bottom_left, top_right = rectangle.get_corner_coordinates(array.shape[0], array.shape[1])

    assert bottom_left.x == 100
    assert bottom_left.y == 0
    assert top_right.x == 200
    assert top_right.y == 500


def test_get_corner_coordinates_width_ne_x(array: np.ndarray):
    origin = Direction.NE
    x = -100
    width = 100

    rectangle = Rectangle(origin=origin, width=width, x=x)
    bottom_left, top_right = rectangle.get_corner_coordinates(array.shape[0], array.shape[1])

    assert bottom_left.x == 300
    assert bottom_left.y == 0
    assert top_right.x == 400
    assert top_right.y == 500


def test_get_corner_coordinates_width_se_x_float(array: np.ndarray):
    origin = Direction.SE
    x = -.2
    y = .2
    width = 100

    rectangle = Rectangle(origin=origin, width=width, x=x, y=y)
    bottom_left, top_right = rectangle.get_corner_coordinates(array.shape[0], array.shape[1])

    assert bottom_left.x == 300
    assert bottom_left.y == 100
    assert top_right.x == 400
    assert top_right.y == 500


def test_get_corner_coordinates_width_c_x(array: np.ndarray):
    origin = Direction.C
    x = -100
    width = 100

    rectangle = Rectangle(origin=origin, width=width, x=x)
    bottom_left, top_right = rectangle.get_corner_coordinates(array.shape[0], array.shape[1])

    assert bottom_left.x == 100
    assert bottom_left.y == 0
    assert top_right.x == 200
    assert top_right.y == 500


def test_get_corner_coordinates_width_c_x_float(array: np.ndarray):
    origin = Direction.C
    x = .2
    width = 100

    rectangle = Rectangle(origin=origin, width=width, x=x)
    bottom_left, top_right = rectangle.get_corner_coordinates(array.shape[0], array.shape[1])

    assert bottom_left.x == 300
    assert bottom_left.y == 0
    assert top_right.x == 400
    assert top_right.y == 500


def test_get_corner_coordinates_width_c_y_float(array: np.ndarray):
    origin = Direction.C
    y = .2
    width = 100

    rectangle = Rectangle(origin=origin, width=width, y=y)
    bottom_left, top_right = rectangle.get_corner_coordinates(array.shape[0], array.shape[1])

    assert bottom_left.x == 200
    assert bottom_left.y == 100
    assert top_right.x == 300
    assert top_right.y == 500


def test_get_corner_coordinates_sw_aspect(array: np.ndarray):
    origin = Direction.SW
    aspect = 2

    rectangle = Rectangle(origin=origin, aspect=aspect)
    bottom_left, top_right = rectangle.get_corner_coordinates(array.shape[0], array.shape[1])

    assert bottom_left.x == 0
    assert bottom_left.y == 0
    assert top_right.x == 500
    assert top_right.y == 250


def test_get_corner_coordinates_ne_aspect(array: np.ndarray):
    origin = Direction.NE
    aspect = .5

    rectangle = Rectangle(origin=origin, aspect=aspect)
    bottom_left, top_right = rectangle.get_corner_coordinates(array.shape[0], array.shape[1])

    assert bottom_left.x == 250
    assert bottom_left.y == 0
    assert top_right.x == 500
    assert top_right.y == 500


def test_get_corner_coordinates_height_sw_aspect(array: np.ndarray):
    origin = Direction.SW
    aspect = 2
    height = 200

    rectangle = Rectangle(origin=origin, height=height, aspect=aspect)
    bottom_left, top_right = rectangle.get_corner_coordinates(array.shape[0], array.shape[1])

    assert bottom_left.x == 0
    assert bottom_left.y == 0
    assert top_right.x == 400
    assert top_right.y == 200


def test_get_corner_coordinates_height_c_aspect_y(array: np.ndarray):
    origin = Direction.C
    aspect = .5
    height = 200
    y = 100

    rectangle = Rectangle(origin=origin, height=height, aspect=aspect, y=y)
    bottom_left, top_right = rectangle.get_corner_coordinates(array.shape[0], array.shape[1])

    assert bottom_left.x == 200
    assert bottom_left.y == 250
    assert top_right.x == 300
    assert top_right.y == 450


def test_get_corner_coordinates_width_n_aspect(array: np.ndarray):
    origin = Direction.N
    aspect = 2
    width = 100

    rectangle = Rectangle(origin=origin, width=width, aspect=aspect)
    bottom_left, top_right = rectangle.get_corner_coordinates(array.shape[0], array.shape[1])

    assert bottom_left.x == 200
    assert bottom_left.y == 450
    assert top_right.x == 300
    assert top_right.y == 500


def test_get_corner_coordinates_width_height_e_aspect(array: np.ndarray):
    """
    aspect is ignored with both width and height
    """
    origin = Direction.E
    aspect = 2
    width = 100
    height = 100

    rectangle = Rectangle(origin=origin, width=width, height=height, aspect=aspect)
    bottom_left, top_right = rectangle.get_corner_coordinates(array.shape[0], array.shape[1])

    assert bottom_left.x == 400
    assert bottom_left.y == 200
    assert top_right.x == 500
    assert top_right.y == 300


def test_cook_width_height_e_aspect(array: np.ndarray):
    """
    aspect is ignored with both width and height
    """
    origin = Direction.E
    aspect = 2
    width = 100
    height = 100

    rectangle = Rectangle(origin=origin, width=width, height=height, aspect=aspect)
    cooked_array = rectangle.cook(array)

    assert np.all(cooked_array[400:500, 200:300] == 255)
