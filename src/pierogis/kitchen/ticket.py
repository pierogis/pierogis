import os
import uuid
from typing import Dict, List

from ..ingredients import Ingredient
from ..ingredients import Pierogi


class PierogiDesc:
    def __init__(self, files_key: str, frame_index: int = 0):
        """

        """
        self.files_key = files_key
        self.frame_index = frame_index

    def create(self, files) -> Pierogi:
        """

        """
        file = files[self.files_key]

        return Pierogi.from_path(path=file, frame_index=self.frame_index)


class IngredientDesc:
    """
    simple json-style representation of an ingredient

    can create a object of itself if given a mapping to its type
    """

    # needs to get type names from types and link them

    def __init__(self, type_name: str, kwargs: dict):
        self.type_name = type_name
        self.kwargs = kwargs

    def create(self, ingredient_classes: dict) -> Ingredient:
        """
        create an ingredient from own args and kwargs

        :param ingredient_classes: map of a type name to an ingredient class
        """
        order = ingredient_classes[self.type_name]
        ingredient = order.type(**self.kwargs)

        return ingredient


class Ticket:
    """describe a dish using a json-like object"""

    output_path: str = None

    @property
    def input_filename(self):
        return os.path.basename(self.input_path)

    @property
    def input_path(self) -> str:
        return self.files[self.pierogis[self.base].files_key]

    @input_path.setter
    def input_path(self, value: str):
        self.files[self.pierogis[self.base].files_key] = value

    def __init__(
            self,
            pierogis: Dict[str, PierogiDesc] = None,
            files: Dict[str, str] = None,
            ingredients: Dict[str, IngredientDesc] = None,
            recipe: List[str] = None,
            base: str = None,
            seasoning_links: Dict[str, str] = None,
            output_path: str = None,
            skip: bool = False
    ):
        """
        create a Ticket
        """
        if pierogis is None:
            pierogis = {}
        if files is None:
            files = {}
        if ingredients is None:
            ingredients = {}
        if recipe is None:
            recipe = []
        if seasoning_links is None:
            seasoning_links = {}

        self.pierogis = pierogis
        self.files = files
        self.ingredients = ingredients
        self.recipe = recipe
        self.base = base
        self.seasoning_links = seasoning_links
        self.output_path = output_path
        self.skip = skip

    def add_file(self, path: str) -> str:
        """
        add a path to files

        :param path: the path to create a file link for
        """
        file_uuid = uuid.uuid4().hex
        self.files[file_uuid] = path

        # this uuid can be used to reference this file
        return file_uuid

    def add_pierogi(self, path, frame_index) -> str:
        pierogi_key = uuid.uuid4().hex

        files_key = self.add_file(path)

        self.pierogis[pierogi_key] = PierogiDesc(
            files_key=files_key, frame_index=frame_index
        )

        return pierogi_key

    def add_ingredient_desc(self, ingredient_desc: IngredientDesc) -> str:
        """
        add an IngredientDesc to ingredients

        :param ingredient_desc: the IngredientDesc to add
        """
        ingredient_key = uuid.uuid4().hex

        self.ingredients[ingredient_key] = ingredient_desc

        return ingredient_key

    def extend_recipe(self, new_instructions: List[str]) -> None:
        """
        add a new list of ingredient uuids to the recipe_order

        :param new_instructions: the IngredientDesc to add
        """
        self.recipe.extend(new_instructions)

    def add_seasoning_link(self, seasoning_key: str, ingredient_key: str) -> None:
        """

        """

        self.seasoning_links[seasoning_key] = ingredient_key


class SeasoningLink:
    def __init__(self, seasoning_key, target_key, recipient_key):
        self.seasoning_key = seasoning_key
        self.target_key = target_key
        self.recipient_keys = recipient_key

    def create(self, ingredients: dict):
        seasoning = ingredients[self.seasoning_key]

        return seasoning
