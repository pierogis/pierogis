from typing import Dict

import numpy as np
import pytest
from PIL import Image

from pierogis.ingredients import Dish, Pierogi
from pierogis.kitchen import LineCook, menu
from pierogis.kitchen.ticket import Ticket, PierogiDesc, IngredientDesc


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
def array():
    return np.asarray(
        [
            [[200, 200, 200], [30, 30, 30], [30, 30, 30]],
            [[130, 130, 130], [60, 60, 60], [30, 30, 30]],
            [[200, 200, 200], [30, 30, 30], [30, 30, 30]],
            [[130, 130, 130], [60, 60, 60], [30, 30, 30]]
        ]
    ).astype(np.dtype('uint8'))


@pytest.fixture
def image_path(array: np.ndarray, tmp_path):
    image = Image.fromarray(array)
    output_path = tmp_path / 'output.png'
    image.save(output_path)

    return output_path


@pytest.fixture
def chef():
    return LineCook()


@pytest.fixture
def image_paths(files_key, image_path) -> Dict[str, str]:
    files = {
        files_key: image_path
    }
    return files


@pytest.fixture
def ingredient_desc(ingredient_key) -> IngredientDesc:
    return IngredientDesc(ingredient_key, kwargs={})


@pytest.fixture
def pierogi_objects(chef, pierogi_key, pierogi_desc, image_paths):
    pierogi_descs = {
        pierogi_key: pierogi_desc
    }
    return chef.create_pierogi_objects(pierogi_descs, image_paths)


@pytest.fixture
def ticket(pierogi_key, pierogi_desc, ingredient_desc, ingredient_key, image_paths):
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
        files=image_paths,
        ingredients=ingredient_descs,
        base=base,
        recipe=[ingredient_key],
        seasoning_links=seasoning_links
    )

    return ticket


@pytest.fixture
def image_dish(image_path: str) -> Dish:
    return Dish(pierogi=Pierogi.from_path(image_path))


def test_create_pierogi_objects(pierogi_objects):
    assert len(pierogi_objects.values()) == 1


def test_create_ingredient_objects(chef, ingredient_desc, pierogi_objects):
    ingredient_descs = {
        ingredient_key: ingredient_desc
    }
    ingredient_objects = chef.create_ingredient_objects(
        ingredient_descs, pierogi_objects, menu.menu
    )

    assert len(ingredient_objects.values()) == 1


def test_get_ingredient_get(chef, ingredient_desc, ingredient_key):
    ingredients = {
        ingredient_key: menu.menu[ingredient_desc.type_name].type()
    }
    ingredient = chef.get_ingredient(
        ingredients,
        {ingredient_key: ingredient_desc},
        ingredient_key,
        menu
    )

    assert ingredients[ingredient_key] == ingredient


def test_get_ingredient_create(chef, ingredient_desc, ingredient_key):
    ingredients = {}
    ingredient = chef.get_ingredient(
        ingredients,
        {ingredient_key: ingredient_desc},
        ingredient_key,
        menu.menu
    )

    order_type = menu.menu[ingredient_desc.type_name].type

    assert order_type == type(ingredient)


def test_assemble_dish(chef, ticket):
    dish = chef.assemble_ticket(ticket, menu.menu)

    assert dish


def test_cook_dish_image(chef, image_dish):
    dish = chef.cook_dish(image_dish)

    assert dish
