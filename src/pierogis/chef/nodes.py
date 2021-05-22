import io
from typing import Callable, Union, Any, Dict

import idom
from idom.widgets import Input

from pierogis.ingredients import Pierogi, Threshold, Sort, Resize, Rotate, Ingredient
from .common import ImageDropArea, SliderInput, Option, SwitchableFieldset
from ..ingredients.seasonings import Seasoning


def SortInput(set_ingredient_callback: Callable[[Sort], None], ingredient: Sort = Sort()):
    if len(ingredient.seasonings) == 0:
        ingredient.season(Threshold())
        set_ingredient_callback(ingredient)

    seasoning = ingredient.seasonings[0]

    def set_seasoning(seasoning: Seasoning):
        ingredient.season(seasoning)
        set_ingredient_callback(ingredient)

    def set_rotate(rotate):
        ingredient.rotate = rotate
        set_ingredient_callback(ingredient)

    return idom.html.div(
        ThresholdInput(set_seasoning, seasoning),
        RotateInput(set_rotate, ingredient.rotate)
    )


def RotateInput(set_ingredient_callback: Callable[[Rotate], None], ingredient: Rotate = Rotate()):
    return


def ResizeInput(set_ingredient_callback: Callable[[Resize], None], ingredient: Resize = Resize()):
    def set_height(height):
        ingredient.height = height
        set_ingredient_callback(ingredient)

    def set_width(width):
        ingredient.width = width
        set_ingredient_callback(ingredient)

    def set_scale(scale):
        ingredient.scale = scale
        set_ingredient_callback(ingredient)

    inputs = [
        "Height",
        Input(
            set_height,
            'number',
            ingredient.height,
            attributes={'min': 0, 'step': 1},
            cast=int
        ),
        "Width",
        Input(
            set_width,
            'number',
            ingredient.width,
            attributes={'min': 0, 'step': 1},
            cast=int
        ),
        "Scale",
        Input(
            set_scale,
            'number',
            ingredient.scale,
            attributes={'min': 0, 'step': .05},
            cast=float
        )
    ]

    return idom.html.div(
        {'style': {'font-size': 'small', 'text-align': 'center'}},
        inputs
    )


def ThresholdInput(
        set_ingredient_callback: Callable[[Threshold], None],
        ingredient: Threshold = Threshold()
):
    def set_lower(lower):
        ingredient.lower_threshold = lower
        set_ingredient_callback(ingredient)

    def set_upper(upper):
        ingredient.upper_threshold = upper
        set_ingredient_callback(ingredient)

    sliders = [
        SliderInput(
            "Lower Threshold",
            ingredient.lower_threshold,
            set_lower,
            (0, 255, 1),
        ),
        SliderInput(
            "Upper Threshold",
            ingredient.upper_threshold,
            set_upper,
            (0, 255, 1),
        )
    ]

    def toggle_inner():
        ingredient.inner = not ingredient.inner
        set_ingredient_callback(ingredient)

    events = idom.Events()

    @events.on("change")
    def on_click(event: Dict[str, Any]) -> None:
        value = event["value"]
        toggle_inner()

    return idom.html.div(
        {'style': {'font-size': 'small', 'text-align': 'center'}},
        sliders,
        "Inner",
        idom.html.br(),
        idom.html.input({'type': 'checkbox', 'checked': ingredient.inner}, event_handlers=events)
        # Input(set_inner, 'checkbox', value="toggle", attributes={'checked': ingredient.inner})
    )


def PierogiInput(set_ingredient_callback: Callable[[Pierogi], Pierogi], ingredient: Pierogi = None):
    def set_image_bytes(image_bytes):
        if image_bytes is None or image_bytes == b'':
            raise Exception('Must have pierogi input')

        set_ingredient_callback(Pierogi.from_path(image_bytes))

    file = io.BytesIO()
    if ingredient is not None:
        ingredient.image.save(file, 'png')
    else:
        Pierogi.from_path(f"https://picsum.photos/800/300?image=1").image.save(file, 'png')
    file.seek(0)
    image_bytes = file.read()

    return idom.html.div(
        {'style': {'width': '200px'}},
        idom.html.fieldset(
            [idom.html.legend({"style": {"font-size": "medium"}}, 'Pierogi')],
            ImageDropArea(set_image_bytes, image_bytes)
        )
    )


threshold_option = Option(name='Threshold', node=ThresholdInput)
sort_option = Option(name='Sort', node=SortInput)
resize_option = Option(name='Resize', node=ResizeInput)
rotate_option = Option(name='Rotate', node=RotateInput)

ingredient_options = {
    Threshold: threshold_option,
    Sort: sort_option,
    Resize: resize_option,
    Rotate: rotate_option,
}


@idom.component
def IngredientNode(
        ingredient: Union[Ingredient, Callable[[Ingredient], Any]],
        set_ingredient_callback: Callable[[Ingredient], Any]
):
    ingredient, set_ingredient = idom.hooks.use_state(ingredient)

    option, set_option = idom.hooks.use_state(ingredient_options[type(ingredient)])

    def update_selected_option(new_selected_option: Option):
        for ingredient_type, option in ingredient_options.items():
            if new_selected_option == option:
                ingredient = ingredient_type()
                set_ingredient_callback(ingredient)
                set_option(new_selected_option)
                set_ingredient(ingredient)
                break

    return idom.html.div(
        {
            'style': {'width': '200px'}
        },
        SwitchableFieldset(
            option,
            list(ingredient_options.values()),
            update_selected_option,
            set_ingredient_callback=set_ingredient_callback, ingredient=ingredient
        ),
    )
