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


def test_create_pierogi_objects(pierogi_objects):
    assert len(pierogi_objects.values()) == 1


def test_create_ingredient_objects(ingredient_desc, pierogi_objects):
    ingredient_descs = {
        ingredient_key: ingredient_desc
    }
    ingredient_objects = Chef.create_ingredient_objects(ingredient_descs, pierogi_objects, menu)

    assert len(ingredient_objects.values()) == 1


def test_get_or_create_ingredient_get(ingredient_descs, ingredient_key):
    ingredients = {
        ingredient_key: menu[ingredient_descs[ingredient_key].type_name].type()
    }
    ingredient = Chef.get_or_create_ingredient(
        ingredients,
        ingredient_descs,
        ingredient_key,
        menu
    )

    assert ingredients[ingredient_key] == ingredient


def test_get_or_create_ingredient_create(ingredient_descs, ingredient_key):
    ingredients = {}
    ingredient = Chef.get_or_create_ingredient(
        ingredients,
        ingredient_descs,
        ingredient_key,
        menu
    )

    order_type = menu[ingredient_descs[ingredient_key].type_name].type

    assert order_type == type(ingredient)


def test_cook_tickets(ticket, image_file):
    order_name = 'test_cook_tickets'
    Chef.cook_tickets(order_name, 'cooked', [ticket], menu)

    order_dir = os.path.join('cooked', order_name)

    output_filename = os.path.join(order_dir, os.path.basename(image_file))

    assert os.path.isdir(order_dir)
    assert os.path.isfile(output_filename)

    os.remove(output_filename)
    os.removedirs(order_dir)
