import io
from collections import namedtuple
from typing import Dict, Any, Callable, TypeVar, List

import idom
from idom import Component
from idom.widgets import Input, image

from pierogis.ingredients import Pierogi


@idom.component
def SliderInput(label, value, set_value_callback, domain):
    minimum, maximum, step = domain
    attrs = {'min': minimum, 'max': maximum, 'step': step}

    value, set_value = idom.hooks.use_state(value)

    def update_value(value: float):
        set_value(value)
        set_value_callback(value)

    return idom.html.div(
        {'class': 'slider-input-container'},
        label,
        idom.html.br(),
        Input(update_value, 'range', value, attributes=dict(attrs, **{'class': 'slider'}), cast=float),
        Input(update_value, 'number', value, attributes=attrs, cast=float)
    )


@idom.component
def ImageDropArea(set_image_bytes_callback, image_bytes: bytes):
    # this is all temporary
    set_image_bytes_callback(image_bytes)
    image_bytes, set_image_bytes = idom.hooks.use_state(image_bytes)

    def update_image_bytes(path):
        file = io.BytesIO()
        Pierogi.from_path(path).image.save(file, 'png')
        file.seek(0)

        new_image_bytes = file.read()
        set_image_bytes(new_image_bytes)
        set_image_bytes_callback(new_image_bytes)

    events = idom.Events()

    @events.on("change")
    def on_change(event: Dict[str, Any], target) -> None:
        print(target)
        value = event["target"]['result']

        update_image_bytes(value)

    args = [
        image('png', image_bytes, attributes={'style': {
            'vertical-align': 'middle',
            'max-width': '90%',
            'max-height': '90%',
            'display': 'block',
            'margin': 'auto'
        }}),
        idom.html.input(
            {
                'id': 'image-input',
                'type': 'file',
                'hidden': True,
                'accept': 'image/*'
            },
            event_handlers=events
        ),
        idom.html.label(
            {
                'class': 'button',
                'for': 'image-input',
                'style': {
                    'display': 'inline-block',
                    'padding': '5px',
                    'padding-left': '10px',
                    'padding-right': '10px',
                    'background': 'white',
                    'cursor': 'pointer',
                    'border-radius': '5px',
                    'border': '1px solid black',
                    'font-size': 'medium'
                },
            },
            'image'
        )
    ]

    return idom.html.div(
        {
            'style': {'border': '1px dotted gray'}
        },
        *args
    )


Option = namedtuple('Option', field_names=['name', 'node'])


def SwitchableFieldset(selected_option: Option, options: List[Option],
                       set_selected_option: Callable[[Option], Any], **kwargs):
    def update_selected_option(event):
        for option in options:
            if option.name == event['value']:
                set_selected_option(option)
                break

    return idom.html.fieldset(
        idom.html.style(
            """
            .slider-input-container {font-size: small; text-align:center}
            .slider-input-container input.slider {width:60%;}
            """
        ),
        idom.html.legend(
            {'style': {'font-size': 'medium'}},
            idom.html.select(
                {'onChange': update_selected_option},
                [idom.html.option(
                    {'selected': selected_option == option},
                    option.name
                ) for option in options]
            )
        ),
        selected_option.node(**kwargs)
    )
