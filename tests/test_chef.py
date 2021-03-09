import os
from typing import List, Dict

import pytest

from pyrogis import Dish
from pyrogis.kitchen import Chef, menu
from pyrogis.kitchen.menu import ResizeOrder
from pyrogis.kitchen.ticket import Ticket, PierogiDesc, IngredientDesc


# @pytest.fixture
# def chef() -> Chef:
#     return Chef()


@pytest.fixture
def pierogi_key():
    return 'pierogi'


@pytest.fixture
def files_key():
    return 'files_key'


@pytest.fixture
def ingredient_key():
    return 'resize'


@pytest.fixture
def pierogi_desc(files_key) -> PierogiDesc:
    return PierogiDesc(files_key=files_key)


@pytest.fixture
def image_file():
    return 'resources/gnome.jpg'


@pytest.fixture
def image_files(files_key, image_file) -> Dict[str, str]:
    files = {
        files_key: image_file
    }
    return files


@pytest.fixture
def ingredient_desc(ingredient_key) -> IngredientDesc:
    return IngredientDesc(ingredient_key, kwargs={})


@pytest.fixture
def pierogi_objects(pierogi_key, pierogi_desc, image_files):
    pierogi_descs = {
        pierogi_key: pierogi_desc
    }
    return Chef.create_pierogi_objects(pierogi_descs, image_files)


@pytest.fixture
def ticket(pierogi_key, pierogi_desc, ingredient_desc, ingredient_key, image_files):
    pierogi_descs = {
        pierogi_key: pierogi_desc
    }

    ingredient_descs = {
        ingredient_key: ingredient_desc
    }

    base = pierogi_key
    seasoning_links = {}

    ticket = Ticket(
        pierogis=pierogi_descs,
        files=image_files,
        ingredients=ingredient_descs,
        base=base,
        recipe=[ingredient_key],
        seasoning_links=seasoning_links
    )

    return ticket


@pytest.fixture
def image_dish() -> Dish:
    return Dish.from_path('resources/gnome.jpg')


@pytest.fixture
def animation_dish() -> Dish:
    return Dish.from_path('resources/octo.mp4')


def test_create_pierogi_objects(pierogi_objects):
    assert len(pierogi_objects.values()) == 1


def test_create_ingredient_objects(ingredient_desc, pierogi_objects):
    ingredient_descs = {
        ingredient_key: ingredient_desc
    }
    ingredient_objects = Chef.create_ingredient_objects(ingredient_descs, pierogi_objects, menu)

    assert len(ingredient_objects.values()) == 1


def test_get_ingredient_get(ingredient_desc, ingredient_key):
    ingredients = {
        ingredient_key: menu[ingredient_desc.type_name].type()
    }
    ingredient = Chef.get_ingredient(
        ingredients,
        {ingredient_key: ingredient_desc},
        ingredient_key,
        menu
    )

    assert ingredients[ingredient_key] == ingredient


def test_get_ingredient_create(ingredient_desc, ingredient_key):
    ingredients = {}
    ingredient = Chef.get_ingredient(
        ingredients,
        {ingredient_key: ingredient_desc},
        ingredient_key,
        menu
    )

    order_type = menu[ingredient_desc.type_name].type

    assert order_type == type(ingredient)


def test_assemble_dish(ticket):
    order_name = 'test_assemble_dish'
    dish = Chef.assemble_ticket(ticket, menu)


def test_cook_dish_image(image_dish):
    order_name = 'test_cook_dish'

    order_dir = os.path.join('cooked', order_name)
    output_filename = os.path.join(order_dir, 'cooked')
    Chef.cook_dish(order_name, 'cooked', output_filename, image_dish)

    assert os.path.isdir(order_dir)
    assert os.path.isfile(output_filename)

    os.remove(output_filename)
    os.removedirs(order_dir)


def test_cook_dish_animation(animation_dish):
    order_name = 'test_cook_dish'

    order_dir = os.path.join('cooked', order_name)
    output_filename = os.path.join(order_dir, os.path.basename(image_file))
    Chef.cook_dish(order_name, 'cooked', output_filename, animation_dish)

    assert os.path.isdir(order_dir)
    assert os.path.isfile(output_filename)

    os.remove(output_filename)
    os.removedirs(order_dir)
