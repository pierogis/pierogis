import io
from typing import List

import idom
from idom import VdomDict, Ref
from idom.widgets.html import image

from pierogis.ingredients import Threshold, Recipe, Dish, Ingredient
from .nodes import IngredientNode, PierogiInput


# def get_recipe(nodes: List[IngredientNode]) -> Recipe:
#     quantize = SpatialQuantize()
#
#     ingredients = [node.ingredient() for node in nodes]
#
#     threshold = Threshold(inner=True, lower_threshold=100, upper_threshold=130)
#     threshold2 = Threshold(inner=True, lower_threshold=100)
#     quantize.season(threshold2)
#     sort = Sort()
#     sort.season(threshold)
#
#     resize = Resize(scale=.5)
#
#     recipe1 = Recipe(ingredients=[resize, sort, quantize, MMPX()])
#     recipe1.season(threshold2)
#
#     recipe = Recipe(ingredients=ingredients)
#
#     return recipe


@idom.component
def Chef():
    output_image, set_output_image = idom.hooks.use_state(image('png'))
    input_pierogi = idom.hooks.use_ref(None)

    ingredients = idom.hooks.use_ref(list())

    def cook() -> VdomDict:
        pierogi = input_pierogi.current
        recipe = Recipe(ingredients=ingredients.current)

        dish = Dish(pierogi=pierogi, recipe=recipe)

        cooked_dish = dish.serve()

        buffer = io.BytesIO()
        cooked_dish.pierogi.image.save(buffer, format='png')
        buffer.seek(0)
        return image('png', buffer.getvalue())

    return idom.html.div(
        output_image,
        PierogiInput(input_pierogi.set_current),
        IngredientNodes(ingredients),
        idom.html.button({"onClick": lambda event: set_output_image(cook())}, "cook"),
    )


def IngredientNodes(
        ingredients_ref: Ref[List[Ingredient]]
):
    nodes, set_nodes = idom.hooks.use_state(
        [IngredientNode(lambda: ingredients_ref.current[i], lambda ingredient: set_ingredient(i, ingredient))
         for i in
         range(len(ingredients_ref.current))])

    def add_ingredient(i):
        threshold = Threshold(lower_threshold=70, upper_threshold=150)
        new_ingredients = ingredients_ref.current.copy()
        new_ingredients.insert(i, threshold)
        ingredients_ref.set_current(new_ingredients)

        new_nodes = nodes.copy()
        new_nodes.insert(i, IngredientNode(lambda: ingredients_ref.current[i],
                                           lambda ingredient: set_ingredient(i, ingredient)))
        set_nodes(new_nodes)

    def del_ingredient(i):
        if len(ingredients_ref.current) > 0:
            new_ingredients = ingredients_ref.current.copy()
            del new_ingredients[i]
            ingredients_ref.set_current(new_ingredients)

            new_nodes = nodes.copy()
            del new_nodes[i]
            set_nodes(new_nodes)

    def set_ingredient(i, ingredient):
        new_ingredients = ingredients_ref.current.copy()
        new_ingredients[i] = ingredient
        ingredients_ref.set_current(new_ingredients)

    return idom.html.div(
        *nodes,
        idom.html.button({"onClick": lambda event: add_ingredient(len(ingredients_ref.current))}, "+"),
        idom.html.button({"onClick": lambda event: del_ingredient(len(ingredients_ref.current) - 1)}, "-"),
    )


def main():
    idom.run(Chef, port=8765)


if __name__ == '__main__':
    main()
