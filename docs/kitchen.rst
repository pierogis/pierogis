kitchen
================

   *"Okay, I lost my mind, it's somewhere out there stranded*

   *I think you stand under me if you don't understand me*

   *Had my heart broken by this woman named Tammy"*

   -- weezy

.. py:currentmodule:: pierogis.kitchen

This submodule defines a model of a kitchen for cooking en masse.
The goal of this is to create an idiom for distributing cooking tasks.

It contains both a protocol of a ``pierogis`` *kitchen* and an implementation.

The protocol is based on :py:class:`~server.Server`, :py:class:`~kitchen.Kitchen`, and :py:class:`~chef.Chef` classes working together to
allow any mode of distributed computing, like multiprocessing, lambda, http, etc.

The implementation here uses :mod:`multiprocessing`.

The protocol defines an :py:class:`~server.OrderTaker` (implemented with :py:class:`~server.Server`) for handling a request for
media to be cooked. The :py:class:`~server.OrderTaker` should transform this into an :py:class:`~order.Order` filled
with :py:class:`~ticket.Ticket` objects to describe each frame. The :py:class:`~server.Server` passes this off to
a :py:class:`~kitchen.Kitchen` which decides how to cook the :py:class:`~order.Order`. Ultimately, a
:py:class:`~chef.Cooker` (implemented with :py:class:`~chef.Chef`) cooks the :py:class:`~ticket.Ticket`
and a cooked :py:class:`~pierogis.ingredients.pierogi.Pierogi` is produced.

- :py:class:`~ticket.Ticket`
  - Describes in a json-friendly format the input media, Ingredient objects, and instructions for a Recipe
- :py:class:`~order.Order`
  - A collection of many tickets and a desciption for handling the :py:class:`~pierogis.course.Course` output as a whole
- :py:class:`~server.Server`
  - Interfaces with instructions provided in a parsable format, creating an :py:class:`~order.Order` for a :py:class:`~kitchen.Kitchen` to process and checking its status
- :py:class:`~chef.Chef`
  - Cooks a ticket and saves it to a specified location
- :py:class:`~kitchen.Kitchen`
  - Cooks an :py:class:`~order.Order` using a :py:class:`~chef.Chef`, possibly distributing the work (multiprocessing, etc.)