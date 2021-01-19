import os

import argparse
import uuid

from pyrogis import Dish, Pierogi, Sort, SpatialQuantize, Threshold, Recipe, Ingredient


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

        :param ingredient_classes: map of a type name assigned to an ingredient class
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
        :param target_uuid: the Seasoning uuid
        """
        self.seasoning_links[target_uuid] = season_uuid


class Chef:
    """
    A class for handling text and json representations of pierogis objects

    Implements parsing into a standard representation and cooking a parsed representation
    """
    ingredient_classes = {
        'pierogi': Pierogi,
        'sort': Sort,
        'quantize': SpatialQuantize,
        'threshold': Threshold
    }

    # seasoning_classes = {
    #     'threshold': Threshold
    # }

    def __init__(self):
        """
        create a Chef
        """
        sort_parser = argparse.ArgumentParser(add_help=False)
        sort_parser.set_defaults(add_dish_desc=self.add_sort_desc)
        Sort.add_parser_arguments(sort_parser)

        threshold_parser = argparse.ArgumentParser(add_help=False)
        threshold_parser.set_defaults(add_dish_desc=self.add_threshold_desc)
        Threshold.add_parser_arguments(threshold_parser)

        quantize_parser = argparse.ArgumentParser(add_help=False)
        quantize_parser.set_defaults(add_dish_desc=self.add_quantize_desc)
        SpatialQuantize.add_parser_arguments(quantize_parser)

        recipe_parser = argparse.ArgumentParser(add_help=False)
        recipe_parser.set_defaults(add_dish_desc=self.add_recipe_desc)
        recipe_parser.add_argument('recipe', type=str, default='sort; quantize')

        self.menu = {
            'sort': sort_parser,
            'quantize': quantize_parser,
            'chef': recipe_parser,
            'threshold': threshold_parser
        }

    def read_recipe(self, dish_description: DishDescription, recipe_text: str):
        """
        read a recipe from string to a DishDescription

        :param dish_description: the dish description to extend
        :param recipe_text: the recipe as a string like 'sort; quantize'
        """
        # split the recipe text by semi colons
        lines = recipe_text.split(';')

        # create the base parser for the recipe text
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()
        # add each parser described by the menu (quantize, sort, etc.)
        for command, command_parser in self.menu.items():
            # add a parser from the given menu item's parser
            subparsers.add_parser(command, parents=[command_parser], add_help=False)

        # now parse each line
        for i in range(len(lines)):
            line = lines[i]
            # line may be just whitespace
            if not line.isspace():
                # split into different words
                phrases = line.strip().split()

                # use the parser with attached subparsers for the recipe names
                parsed, unknown = parser.parse_known_args(phrases)
                parsed_vars = vars(parsed)

                # this will correspond to one of the menu item's parser's link to a method on this class
                add_dish_desc = parsed_vars.pop('add_dish_desc')

                dish_description = add_dish_desc(dish_description, **parsed_vars)

        return dish_description

    def add_recipe_desc(self, dish_desc: DishDescription, recipe: str, path=None, **kwargs):
        """
        add to dish_desc using a recipe specified in a string or a file
        """
        if path is not None:
            dish_desc = self.add_pierogi_desc(dish_desc, path)

        # recipe can be provided as a string
        recipe_text = recipe

        # get recipe from file if this is a file
        if os.path.isfile(recipe):
            with open(recipe) as recipe_file:
                recipe_text = recipe_file.read()

        dish_desc = self.read_recipe(dish_desc, recipe_text)

        return dish_desc

    def add_pierogi_desc(self, dish_desc: DishDescription, path: str):
        """
        add a Pierogi IngredientDesc to and extend the recipe of dish_desc

        :param dish_desc: dish_desc to be extended
        :param path: path to be used to get the file of this Pierogi
        """
        file_uuid = dish_desc.add_file_link(path)

        ingredient_desc = IngredientDesc(
            type_name='pierogi',
            args=[],
            kwargs={
                'file': file_uuid
            }
        )

        # update the dish_desc
        pierogi_uuid = dish_desc.add_ingredient_desc(ingredient_desc)
        dish_desc.extend_recipe([pierogi_uuid])

        return dish_desc

    def add_threshold_desc(self, dish_desc: DishDescription, path=None, **kwargs):
        """
        Add a threshold recipe to the dish description
        """
        if path is not None:
            dish_desc = self.add_pierogi_desc(dish_desc, path)

        ingredient_desc = IngredientDesc(
            type_name='threshold',
            args=[],
            kwargs={
                **kwargs
            }
        )

        # update the dish_desc
        threshold_uuid = dish_desc.add_ingredient_desc(ingredient_desc)
        dish_desc.extend_recipe([threshold_uuid])

        return dish_desc

    def add_sort_desc(self, dish_desc: DishDescription, path: str = None, **kwargs):
        """
        Sort pixels in an image by intensity
        """
        if path is not None:
            dish_desc = self.add_pierogi_desc(dish_desc, path)

        # seasoning is for things that process but don't return a array
        sort_desc = IngredientDesc(
            type_name='sort',
            args=[],
            kwargs={
                **kwargs
            }
        )
        sort_uuid = dish_desc.add_ingredient_desc(sort_desc)

        # check for implied threshold
        lower_threshold = kwargs.pop('lower_threshold')
        upper_threshold = kwargs.pop('upper_threshold')
        if (lower_threshold is not None) or (upper_threshold is not None):
            threshold_desct = IngredientDesc(
                type_name='threshold',
                args=[],
                kwargs={
                    'lower_threshold': lower_threshold,
                    'upper_threshold': upper_threshold
                }
            )
            season_uuid = dish_desc.add_ingredient_desc(threshold_desct)
            dish_desc.add_seasoning(sort_uuid, season_uuid)

        dish_desc.extend_recipe([sort_uuid])

        return dish_desc

    def add_quantize_desc(self, dish_desc: DishDescription, path: str = None, **kwargs):
        """
        Create a description of a quantize recipe
        """
        if path is not None:
            dish_desc = self.add_pierogi_desc(dish_desc, path)

        quantize_desc = IngredientDesc(
            type_name='quantize',
            args=[],
            kwargs=kwargs
        )

        quantize_uuid = dish_desc.add_ingredient_desc(quantize_desc)

        dish_desc.extend_recipe([quantize_uuid])

        return dish_desc

    def create_ingredient_objects(self, ingredient_descs: dict, file_links: dict):
        """
        create a dict of uuid->Ingredient from an ingredient description and a lookup for file paths

        :param ingredient_descs: map of uuid keys to inner dict with type, args, and kwargs keys
        :param file_links: map of uuid keys to file paths, usually for Pierogi
        """
        ingredients = {}

        for ingredient_name, ingredient_desc in ingredient_descs.items():
            # if path is one of the kwargs, we should look it up in the linking paths dictionary
            file_name = ingredient_desc.kwargs.get('file')
            if file_name is not None:
                file = file_links[file_name]
                ingredient_desc.kwargs['file'] = file

            # now create an ingredient as specified in the description
            ingredient = ingredient_desc.create(self.ingredient_classes)

            ingredients[ingredient_name] = ingredient

        return ingredients

    def create_recipe_object(self, ingredients: dict, seasoning_links: dict, recipe_order: list):
        """
        create a recipe from ingredients map, seasoning name map, and order of ingredients

        :param ingredients: map of uuid key to ingredient object value
        :param seasoning_links: map of "recipient ingredient" uuid keys to seasoning uuid values
        :param recipe_order: order of ingredients by uuid
        """
        recipe = Recipe(ingredients=[])

        for ingredient_name in recipe_order:
            # loop through the ingredient keys specified by the recipe

            # there might be a bug here with the ingredient being out
            # of sync with another reference to that ingredient
            ingredient = ingredients[ingredient_name]

            # if there is a season to be applied to this ingredient
            seasoning_name = seasoning_links.get(ingredient_name)
            if seasoning_name is not None:
                # get the ingredient to apply the season
                seasoning = ingredients[seasoning_name]
                # by default a seasoning's target should be the first ingredient in the recipe
                if seasoning.target is None:
                    seasoning.target = recipe.ingredients[0]

                # now seasoning should cook the first ingredient's pixel array
                # and apply that as the mask on ingredient
                seasoning.season(ingredient)

            # add this created ingredient to the dish recipe for return
            recipe.add(ingredient)

        return recipe

    def cook_dish_desc(self, dish_description: DishDescription):
        """
        Cook a dish from a series of descriptive dicts
        """
        ingredient_descs = dish_description.ingredients
        file_links = dish_description.file_links
        recipe_order = dish_description.recipe_order
        seasoning_links = dish_description.seasoning_links

        ingredients = self.create_ingredient_objects(ingredient_descs, file_links)

        recipe = self.create_recipe_object(ingredients, seasoning_links, recipe_order)

        dish = Dish(recipe=recipe)
        return dish.serve()
