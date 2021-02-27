import os
from typing import Dict, List

from .ticket import Ticket
from ..ingredients import (
    Ingredient, Dish, Pierogi, Recipe
)


class Chef:
    """
    handles text and json representations of pierogis constructs

    implements parsing into a standard representation
    and cooking a parsed representation
    """

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
        ingredients: Dict[str, Ingredient] = {}

        for ingredient_name, ingredient_desc in ingredient_descs.items():
            # if path is one of the kwargs
            # look it up in the linking paths dictionary
            pierogi_name = ingredient_desc.kwargs.get('pierogi')
            if pierogi_name is not None:
                pierogi = pierogis[pierogi_name]
                ingredient_desc.kwargs['pierogi'] = pierogi

            ingredient = self.get_or_create_ingredient(
                ingredients, ingredient_descs, ingredient_name
            )

            ingredients[ingredient_name] = ingredient

        return ingredients

    def get_or_create_ingredient(
            self,
            ingredients: dict,
            ingredient_descs: dict,
            ingredient_name: str,
            menu: dict
    ):
        """
        look to see if an ingredient object has already been created
        otherwise create it and swap it in the ingredients dictionary
        """
        ingredient = ingredients.get(ingredient_name)

        if ingredient is None:
            ingredient_desc = ingredient_descs[ingredient_name]

            # search kwargs for keys that are type names
            # swap the value of that kwarg (reference key)
            # for the created ingredient obj
            for ingredient_type_name in menu.keys():
                ingredient_name = ingredient_desc.kwargs.get(
                    ingredient_type_name
                )

                if ingredient_name is not None:
                    ingredient = self.get_or_create_ingredient(
                        ingredients, ingredient_descs, ingredient_name, menu
                    )
                    ingredient_desc.kwargs[ingredient_type_name] = ingredient

            # now create an ingredient as specified in the description
            ingredient = ingredient_desc.create(menu)

        return ingredient

    def apply_seasonings(self, ingredients, seasoning_links):
        for seasoning, recipient in seasoning_links.items():
            seasoning = ingredients[seasoning]
            recipient = ingredients[recipient]

            recipient.season(seasoning)

    def create_recipe_object(
            self,
            ingredients: Dict[str, Ingredient],
            recipe_order: List[str]
    ):
        """
        create a recipe from:
        ingredients map
        seasoning name map
        order of ingredients

        :param ingredients: map of uuid key to ingredient object value
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

    def cook_tickets(self, order_name, tickets: List[Ticket]) -> None:
        """
        cook a dish from a series of descriptive dicts
        """
        cooked_dishes = []

        for ticket in tickets:
            pierogi_descs = ticket.pierogis
            ingredient_descs = ticket.ingredients
            files = ticket.files
            recipe = ticket.recipe
            base = ticket.base
            seasoning_links = ticket.seasoning_links

            pierogis = self.create_pierogi_objects(
                pierogi_descs,
                files
            )

            ingredients = self.create_ingredient_objects(
                ingredient_descs,
                pierogis
            )

            self.apply_seasonings(
                ingredients,
                seasoning_links
            )

            recipe_object = self.create_recipe_object(
                ingredients,
                recipe
            )

            dish = Dish(
                pierogis=[pierogis[base]],
                recipe=recipe_object
            )

            output_path = os.path.join('cooked', order_name, os.path.basename(pierogis[base].file))

            cooked_dish = dish.serve()
            cooked_dish.save(output_path)
