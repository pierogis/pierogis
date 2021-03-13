from typing import Dict, List

from .menu import MenuItem
from .ticket import Ticket, PierogiDesc, IngredientDesc
from ..ingredients import (
    Ingredient, Dish, Pierogi, Recipe
)


class Chef:
    """
    handles text and json representations of pierogis constructs

    implements parsing into a standard representation
    and cooking a parsed representation
    """

    @classmethod
    def create_pierogi_objects(
            cls,
            pierogi_descs: Dict[str, PierogiDesc],
            files: Dict[str, str]
    ) -> Dict[str, Pierogi]:
        """
        exchange a set of PierogiDesc keyed by a name
        with Pierogi loaded from file links
        """
        pierogi_objects = {}

        for pierogi_key, pierogi_desc in pierogi_descs.items():
            pierogi_obj = pierogi_desc.create(files)

            pierogi_objects[pierogi_key] = pierogi_obj

        return pierogi_objects

    @classmethod
    def create_ingredient_objects(
            cls,
            ingredient_descs: Dict[str, IngredientDesc],
            pierogis: Dict[str, Pierogi],
            menu: Dict[str, MenuItem]
    ) -> Dict[str, Ingredient]:
        """
        create a dict of uuid->Ingredient
        from an ingredient description and a lookup for file paths

        :param ingredient_descs: map of uuid keys to inner dict
        with type, args, and kwargs keys
        :param pierogis: map of uuid keys created Pierogi
        """
        ingredients: Dict[str, Ingredient] = {}

        for ingredient_name, ingredient_desc in ingredient_descs.items():
            # if path is one of the kwargs
            # look it up in the linking paths dictionary
            pierogi_name = ingredient_desc.kwargs.get('pierogi')
            if pierogi_name is not None:
                pierogi = pierogis[pierogi_name]
                ingredient_desc.kwargs['pierogi'] = pierogi

            ingredient = cls.get_ingredient(
                ingredients, ingredient_descs, ingredient_name, menu
            )

            ingredients[ingredient_name] = ingredient

        return ingredients

    @classmethod
    def get_ingredient(
            cls,
            ingredients: dict,
            ingredient_descs: Dict[str, IngredientDesc],
            ingredient_name: str,
            menu: dict
    ) -> Ingredient:
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
                    ingredient = cls.get_ingredient(
                        ingredients, ingredient_descs, ingredient_name, menu
                    )
                    ingredient_desc.kwargs[ingredient_type_name] = ingredient

            # now create an ingredient as specified in the description
            ingredient = ingredient_desc.create(menu)

        return ingredient

    @classmethod
    def apply_seasonings(cls, ingredients, seasoning_links) -> None:
        for seasoning, recipient in seasoning_links.items():
            seasoning = ingredients[seasoning]
            recipient = ingredients[recipient]

            recipient.season(seasoning)

    @classmethod
    def create_recipe_object(
            cls,
            ingredients: Dict[str, Ingredient],
            recipe_order: List[str]
    ) -> Recipe:
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

    @classmethod
    def assemble_ticket(cls, ticket: Ticket, menu: Dict) -> Dish:
        """
        cook a dish from a series of descriptive dicts
        """
        pierogi_descs = ticket.pierogis
        ingredient_descs = ticket.ingredients
        files = ticket.files
        recipe = ticket.recipe
        base = ticket.base
        seasoning_links = ticket.seasoning_links

        pierogis = cls.create_pierogi_objects(
            pierogi_descs,
            files
        )

        ingredients = cls.create_ingredient_objects(
            ingredient_descs,
            pierogis,
            menu
        )

        cls.apply_seasonings(
            ingredients,
            seasoning_links
        )

        recipe_object = cls.create_recipe_object(
            ingredients,
            recipe
        )

        return Dish(
            pierogis=[pierogis[base]],
            recipe=recipe_object
        )

    @classmethod
    def cook_dish(
            cls,
            dish: Dish
    ) -> Dish:
        """

        """
        return dish.serve()
