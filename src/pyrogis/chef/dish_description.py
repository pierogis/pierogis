import uuid

from ..ingredients import Ingredient


class IngredientDesc:
    """
    simple json-style representation of an ingredient

    can create a object of itself if given a mapping to its type
    """

    # needs to get type names from types and link them

    def __init__(self, type_name: str, args: list, kwargs: dict):
        self.type_name = type_name
        self.args = args
        self.kwargs = kwargs

    def create(self, ingredient_classes: dict) -> Ingredient:
        """
        create an ingredient from own args and kwargs

        :param ingredient_classes: map of a type name to an ingredient class
        """
        ingredient_type = ingredient_classes[self.type_name]
        ingredient = ingredient_type(*self.args, **self.kwargs)

        return ingredient


class DishDescription:
    """
    describe a dish using a json style object
    """

    def __init__(self, ingredients: dict = None, seasoning_links: dict = None,
                 recipe_order: list = None, file_links: dict = None
                 ):
        """
        create a DishDescription
        """
        if ingredients is None:
            ingredients = {}
        if seasoning_links is None:
            seasoning_links = {}
        if recipe_order is None:
            recipe_order = []
        if file_links is None:
            file_links = {}

        self.ingredients = ingredients
        self.seasoning_links = seasoning_links
        self.recipe_order = recipe_order
        self.file_links = file_links

    def add_ingredient_desc(self, ingredient_desc: IngredientDesc):
        """
        add an IngredientDesc to ingredients

        :param ingredient_desc: the IngredientDesc to add
        """
        pierogi_uuid = str(uuid.uuid4())

        self.ingredients[pierogi_uuid] = ingredient_desc

        return pierogi_uuid

    def add_file_link(self, path: str):
        """
        add a path to file links

        :param path: the path to create a file link for
        """
        file_uuid = str(uuid.uuid4())
        self.file_links[file_uuid] = path

        # this uuid can be used to reference this file
        return file_uuid

    def extend_recipe(self, new_instructions: list):
        """
        add a new list of ingredient uuids to the recipe_order

        :param new_instructions: the IngredientDesc to add
        """
        self.recipe_order.extend(new_instructions)

    def add_seasoning(self, target_uuid, season_uuid):
        """
        add a seasoning instruction to the seasoning_links

        :param target_uuid: the target uuid
        :param season_uuid: the Seasoning uuid
        """
        self.seasoning_links[target_uuid] = season_uuid
