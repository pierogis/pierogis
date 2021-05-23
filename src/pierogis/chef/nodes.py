import io
from typing import Callable, Union, Any

import idom
from idom.widgets import Input

from pierogis.ingredients import Pierogi, Threshold, Sort, Resize, Rotate, Ingredient, MMPX, SpatialQuantize, Quantize
from .common import ImageDropArea, SliderInput, Option, SwitchableFieldset, CheckboxInput, SelectInput, ColorInput
from ..ingredients.seasonings import Seasoning


def QuantizeInput(
        set_ingredient_callback: Callable[[Union[Quantize, SpatialQuantize]], None],
        ingredient: Union[Quantize, SpatialQuantize] = SpatialQuantize()
):
    dither = isinstance(ingredient, SpatialQuantize)

    # def set_palette_size(palette_size: int):
    #     ingredient.palette_size = palette_size
    #     set_ingredient_callback(ingredient)

    def set_dither(dither: bool):
        if dither:
            set_ingredient_callback(SpatialQuantize())
        else:
            set_ingredient_callback(Quantize())

    inputs = [CheckboxInput('dither', dither, set_dither)]

    return idom.html.div(
        {'style': {'font-size': 'small', 'text-align': 'center'}},
        SpatialQuantizeInput(set_ingredient_callback, ingredient)
    )


def SpatialQuantizeInput(set_ingredient_callback: Callable, ingredient: SpatialQuantize = SpatialQuantize()):
    def set_palette_size(value: int):
        ingredient.palette_size = value
        set_ingredient_callback(ingredient)

    inputs = [
        idom.html.div(
            {'style': {'font-size': 'small', 'text-align': 'center'}},
            "palette size",
            Input(set_palette_size, 'number', ingredient.palette_size, cast=int)
        ),
        ColorInput()
    ]

    return idom.html.div(
        inputs
    )


# def PaletteQuantizeInput():
#     def set_colors(value):
#         ingredient.colors = value
#         set_ingredient_callback()
#
#     return idom.html.div(
#         ColorInput(set_colors)
#     )


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
        idom.html.hr(),
        RotateInput(set_rotate, ingredient.rotate)
    )


def RotateInput(set_ingredient_callback: Callable[[Rotate], None], ingredient: Rotate = Rotate()):
    def set_angle(angle):
        ingredient.angle = angle
        set_ingredient_callback(ingredient)

    def set_turns(turns):
        ingredient.turns = turns
        set_ingredient_callback(ingredient)

    def set_ccw(clockwise):
        ingredient.clockwise = clockwise
        set_ingredient_callback(ingredient)

    def set_filter(option):
        ingredient.filter = ingredient.FILTERS[option]
        set_ingredient_callback(ingredient)

    return idom.html.div(
        SliderInput("angle", ingredient.angle, set_angle, (0, 360, 1)),
        idom.html.div(
            {'style': {'font-size': 'small', 'text-align': 'center'}},
            "turns",
            Input(set_turns, 'number', ingredient.turns, cast=float)
        ),
        CheckboxInput("clockwise", ingredient.clockwise, set_ccw),
        SelectInput("filter", ingredient.resample, ingredient.FILTERS.keys(), set_filter)
    )


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

    def set_filter(option):
        ingredient.filter = ingredient.FILTERS[option]
        set_ingredient_callback(ingredient)

    inputs = [
        "height",
        Input(
            set_height,
            'number',
            ingredient.height,
            attributes={'min': 0, 'step': 1},
            cast=int
        ),
        "width",
        Input(
            set_width,
            'number',
            ingredient.width,
            attributes={'min': 0, 'step': 1},
            cast=int
        ),
        "scale",
        Input(
            set_scale,
            'number',
            ingredient.scale,
            attributes={'min': 0, 'step': .05},
            cast=float
        ),
        SelectInput("filter", ingredient.resample, ingredient.FILTERS.keys(), set_filter)
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
            "lower",
            ingredient.lower_threshold,
            set_lower,
            (0, 255, 1),
        ),
        SliderInput(
            "upper",
            ingredient.upper_threshold,
            set_upper,
            (0, 255, 1),
        )
    ]

    def toggle_inner(value):
        ingredient.inner = value
        set_ingredient_callback(ingredient)

    return idom.html.div(
        sliders,
        CheckboxInput("inner", ingredient.inner, toggle_inner)
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
            [idom.html.legend({"style": {"font-size": "medium"}}, 'pierogi')],
            ImageDropArea(set_image_bytes, image_bytes)
        )
    )


threshold_option = Option(name='threshold', node=ThresholdInput)
sort_option = Option(name='sort', node=SortInput)
quantize_option = Option(name='quantize', node=QuantizeInput)
resize_option = Option(name='resize', node=ResizeInput)
rotate_option = Option(name='rotate', node=RotateInput)
mmpx_option = Option(name='mmpx', node=lambda **kwargs: '')

ingredient_options = {
    Threshold: threshold_option,
    Sort: sort_option,
    Resize: resize_option,
    Rotate: rotate_option,
    MMPX: mmpx_option,
    SpatialQuantize: quantize_option,
    # Quantize: quantize_option,
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
