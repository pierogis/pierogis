import uuid

from ..ingredients import Ingredient
from ..ingredients import Pierogi


class PierogiDesc:
    def __init__(self, files_key):
        self.files_key = files_key

    def create(self, files):
        file = files[self.files_key]

        return Pierogi(file=file)


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
        ingredient_type = ingredient_classes[self.type_name]
        ingredient = ingredient_type(**self.kwargs)

        return ingredient


class DishDescription:
    """
    describe a dish using a json style object
    """

    def __init__(
            self, pierogis: dict = None, files: dict = None,
            ingredients: dict = None, dish: list = None,
            seasoning_links: dict = None
    ):
        """
        create a DishDescription
        """
        if pierogis is None:
            pierogis = {}
        if files is None:
            files = {}
        if ingredients is None:
            ingredients = {}
        if dish is None:
            dish = {
                'pierogi': None,
                'recipe': []
            }
        if seasoning_links is None:
            seasoning_links = {}

        self.pierogis = pierogis
        self.files = files
        self.ingredients = ingredients
        self.dish = dish
        self.seasoning_links = seasoning_links

    def add_file(self, path: str):
        """
        add a path to files

        :param path: the path to create a file link for
        """
        file_uuid = str(uuid.uuid4())
        self.files[file_uuid] = path

        # this uuid can be used to reference this file
        return file_uuid

    def add_pierogi_desc(self, path):
        pierogi_key = str(uuid.uuid4())

        files_key = self.add_file(path)

        self.pierogis[pierogi_key] = PierogiDesc(files_key=files_key)

        return pierogi_key

    def add_ingredient_desc(self, ingredient_desc: IngredientDesc):
        """
        add an IngredientDesc to ingredients

        :param ingredient_desc: the IngredientDesc to add
        """
        ingredient_key = str(uuid.uuid4())

        self.ingredients[ingredient_key] = ingredient_desc

        return ingredient_key

    def extend_recipe(self, new_instructions: list):
        """
        add a new list of ingredient uuids to the recipe_order

        :param new_instructions: the IngredientDesc to add
        """
        self.dish['recipe'].extend(new_instructions)

    def add_seasoning_link(self, seasoning_key, ingredient_key):
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
