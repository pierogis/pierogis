import io
from collections import namedtuple
from typing import Dict, Any, Callable, List

import idom
from idom.widgets import Input, image

from pierogis.ingredients import Pierogi


@idom.component
def SliderInput(label: str, value, set_value_callback: Callable, domain):
    minimum, maximum, step = domain
    attrs = {'min': minimum, 'max': maximum, 'step': step}

    value, set_value = idom.hooks.use_state(value)

    def update_value(value: float):
        set_value(value)
        set_value_callback(value)

    return idom.html.div(
        {'class': 'input-container'},
        label,
        idom.html.br(),
        Input(update_value, 'range', value, attributes=attrs, cast=float),
        Input(update_value, 'number', value, attributes=attrs, cast=float)
    )


@idom.component
def CheckboxInput(label, checked: bool, set_checked_callback: Callable):
    checked, set_checked = idom.hooks.use_state(checked)

    def update_value(value: str):
        set_checked(not checked)
        set_checked_callback(not checked)

    if checked:
        checked_key = {'checked': True}
    else:
        checked_key = {'checked': ''}

    return idom.html.div(
        {'class': 'input-container'},
        label,
        idom.html.br(),
        Input(update_value, 'checkbox', value='toggle', attributes=checked_key)
    )


def SelectInput(label, selected_option: str, options: List[str], set_selected_option_callback: Callable):
    def update_selected_option(event: Dict[str, str]):
        set_selected_option_callback(event['value'])

    return idom.html.div(
        {'class': 'input-container'},
        label,
        idom.html.br(),
        idom.html.select(
            {'onChange': update_selected_option},
            [idom.html.option(
                {'selected': selected_option == option},
                option
            ) for option in options]
        )
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
    def on_change(event: Dict[str, Any]) -> None:
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
    async def update_selected_option(event):
        for option in options:
            if option.name == event['value']:
                set_selected_option(option)
                break

    return idom.html.fieldset(
        idom.html.style(
            """
            .input-container {font-size: small; text-align:center}
            .input-container input[type="range"] {width:60%;}
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


def Loader():
    return idom.html.div(
        {'style', {
            'border': '16px solid',
            'border-top': '16px solid',
            'border-radius': '50 %',
            'width': '120px',
            'height': '120px',
            'animation': 'spin 2s linear infinite'
        }},
        idom.html.style("""
            @keyframes spin {
              0% { transform: rotate(0deg); }
              100% { transform: rotate(360deg); }
            }
        """)
    )


def ColorInput():
    return None
