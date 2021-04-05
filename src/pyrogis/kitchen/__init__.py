"""
>*"Okay, I lost my mind, it's somewhere out there stranded*
>
>*I think you stand under me if you don't understand me*
>
>*Had my heart broken by this woman named Tammy"*
>
>\- weezy

This submodule defines a model of a kitchen for cooking `Pierogi` en masse.
The goal of this is to create an idiom for distributing cooking tasks.

It contains both a protocol of a `pierogis` kitchen and an implementation.

The protocol is based on Server, Kitchen, and Chef classes working together to
allow any mode of distributed computing, like multiprocessing, lambda, http, etc.

The implementation here uses multiprocessing.

The protocol defines an `OrderTaker` (`Server`) for handling a requests for
media to be cooked. The `OrderTaker` should transform this into an `Order` filled
with `Ticket` objects to describe each frame. The Server passes this off to
a `Kitchen` which decides how to cook the `Order`. Ultimately, a
`Cooker` (`Chef`) cooks the `Ticket` and a cooked `Pierogi` is produced.

- `Ticket`
  - Describes in a json-friendly format the input media, Ingredient objects,
    and instructions for a Recipe
- `Order`
  - A collection of many tickets and a desciption for handling the `Course`
    output as a whole
- `Server`
  - Interfaces with instructions provided in a parsable format, creating
    an `Order` for a `Kitchen` to process and checking its status
- `Chef`
  - Cooks a ticket and saves it to a specified location
- `Kitchen`
  - Cooks an `Order` using a `Chef`, possibly distributing the work
    (multiprocessing, etc.)
"""

from .chef import Chef
from .kitchen import Kitchen
from .menu import menu
from .order import Order
from .server import Server
from .ticket import Ticket

__all__ = [
    'Chef',
    'Server',
    'Kitchen',
    'Ticket',
    'Order'
]
