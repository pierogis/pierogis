from .dish_description import DishDescription
from .menu import menu
from ..ingredients import (
    Dish, Pierogi, Sort,
    SpatialQuantize, Threshold, Recipe
)


class Chef:
    """
    handles text and json representations of pierogis constructs

    implements parsing into a standard representation
    and cooking a parsed representation
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

    menu = menu

    def create_ingredient_objects(
            self,
            ingredient_descs: dict,
            file_links: dict
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
            file_name = ingredient_desc.kwargs.get('file')
            if file_name is not None:
                file = file_links[file_name]
                ingredient_desc.kwargs['file'] = file

            # now create an ingredient as specified in the description
            ingredient = ingredient_desc.create(self.ingredient_classes)

            ingredients[ingredient_name] = ingredient

        return ingredients

    def create_recipe_object(
            self,
            ingredients: dict,
            seasoning_links: dict,
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
                # by default a seasoning's target
                # is the first ingredient in the recipe
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
        cook a dish from a series of descriptive dicts
        """
        ingredient_descs = dish_description.ingredients
        file_links = dish_description.file_links
        recipe_order = dish_description.recipe_order
        seasoning_links = dish_description.seasoning_links

        ingredients = self.create_ingredient_objects(
            ingredient_descs,
            file_links
        )

        recipe = self.create_recipe_object(
            ingredients,
            seasoning_links,
            recipe_order
        )

        dish = Dish(recipe=recipe)
        return dish.serve()
