from .dish_description import DishDescription
from .menu import menu
from ..ingredients import (
    Dish, Pierogi, Sort,
    SpatialQuantize, Threshold, Recipe, Rotate
)


class Chef:
    """
    handles text and json representations of pierogis constructs

    implements parsing into a standard representation
    and cooking a parsed representation
    """
    ingredient_classes = {
        'sort': Sort,
        'quantize': SpatialQuantize,
        'threshold': Threshold,
        'rotate': Rotate
    }

    # seasoning_classes = {
    #     'threshold': Threshold
    # }

    menu = menu

    def create_pierogi_objects(self, pierogi_descs: dict, file_links: dict):
        pierogi_objects = {}

        for pierogi_key, pierogi_desc in pierogi_descs.items():
            file = file_links[pierogi_desc.files_key]
            pierogi = Pierogi(file=file)

            pierogi_objects[pierogi_key] = pierogi

        return pierogi_objects

    def create_ingredient_objects(
            self,
            ingredient_descs: dict,
            pierogis: dict
    ):
        """
        create a dict of uuid->Ingredient
        from an ingredient description and a lookup for file paths

        :param ingredient_descs: map of uuid keys to inner dict
        with type, args, and kwargs keys
        :param file_links: map of uuid keys to file paths,
        usually for Pierogi
        """
        ingredients = {}

        for ingredient_name, ingredient_desc in ingredient_descs.items():
            # if path is one of the kwargs
            # look it up in the linking paths dictionary
            pierogi_name = ingredient_desc.kwargs.get('pierogi')
            if pierogi_name is not None:
                pierogi = pierogis[pierogi_name]
                ingredient_desc.kwargs['pierogi'] = pierogi

            ingredient = self.get_or_create_ingredient(ingredients, ingredient_descs, ingredient_name)

            ingredients[ingredient_name] = ingredient

        return ingredients

    def get_or_create_ingredient(self, ingredients: dict, ingredient_descs: dict, ingredient_name):
        ingredient = ingredients.get(ingredient_name)

        if ingredient is None:
            ingredient_desc = ingredient_descs[ingredient_name]

            # search kwargs for keys that are type names
            # swap the value of that kwarg (reference key) for the built ingredient
            for ingredient_type_name in self.ingredient_classes.keys():
                ingredient_name = ingredient_desc.kwargs.get(ingredient_type_name)

                if ingredient_name is not None:
                    ingredient = self.get_or_create_ingredient(ingredients, ingredient_descs, ingredient_name)
                    ingredient_desc.kwargs[ingredient_type_name] = ingredient

            # now create an ingredient as specified in the description
            ingredient = ingredient_desc.create(self.ingredient_classes)

        return ingredient

    def apply_seasonings(self, ingredients, seasoning_links):
        for seasoning, recipient in seasoning_links.items():
            seasoning = ingredients[seasoning]
            recipient = ingredients[recipient]

            seasoning.season(recipient)

    def create_recipe_object(
            self,
            ingredients: dict,
            recipe_order: list
    ):
        """
        create a recipe from:
        ingredients map
        seasoning name map
        order of ingredients

        :param ingredients: map of uuid key to ingredient object value
        :param seasoning_links: map of "recipient ingredient" uuid keys
        to seasoning uuid values
        :param recipe_order: order of ingredients by uuid
        """

        recipe = Recipe(ingredients=[])
        # loop through the ingredient keys specified by the recipe
        for ingredient_key in recipe_order:
            # there might be a bug here with the ingredient being out
            # of sync with another reference to that ingredient
            ingredient = ingredients[ingredient_key]

            # add this created ingredient to the dish recipe for return
            recipe.add(ingredient)

        return recipe

    def cook_dish_desc(self, dish_description: DishDescription):
        """
        cook a dish from a series of descriptive dicts
        """
        pierogi_descs = dish_description.pierogis
        ingredient_descs = dish_description.ingredients
        file_links = dish_description.files
        dish = dish_description.dish
        seasoning_links = dish_description.seasoning_links

        pierogis = self.create_pierogi_objects(
            pierogi_descs,
            file_links
        )

        ingredients = self.create_ingredient_objects(
            ingredient_descs,
            pierogis
        )

        self.apply_seasonings(
            ingredients,
            seasoning_links
        )

        recipe = self.create_recipe_object(
            ingredients,
            dish['recipe']
        )

        dish = Dish(
            pierogis=[pierogis[dish['pierogi']]],
            recipe=recipe
        )
        return dish.serve()
