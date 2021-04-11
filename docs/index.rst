pierogis
================

*image and animation processing framework*

   "``pierogis`` *is the name of the framework;*

   ``pyrogis`` *is the name of the python package and cli tool"*

   \- a wise man

.. currentmodule:: pyrogis.ingredients

Pixel arrays (like images) stored as a :py:class:`~pierogi.Pierogi` object can be cooked
with an :py:class:`~ingredient.Ingredient`
such as :py:class:`~sort.Sort`, :py:class:`~quantize.Quantize`,
and :py:class:`~resize.Resize`.

A :py:class:`~dish.Dish` can be made with a :py:class:`~recipe.Recipe` containing
several :py:class:`~ingredient.Ingredient` objects describing a pipeline
to be applied to a :py:class:`~pierogi.Pierogi`.

A :py:class:`~pyrogis.course.Course` can be made to cook a set of
:py:class:`~dish.Dish` objects representing frames
that compile to a cooked animation.

.. currentmodule:: pyrogis.kitchen.menu

A :doc:`rich <rich:introduction>` cli uses :py:class:`~filling.Filling`
objects to parse orders into cook tasks as a :py:class:`~pyrogis.restaurant.Restaurant`.
These can be found on the :doc:`menu`.

In this realm, a single `pierogi` means a pixel, many `pierogi` means an image, and `pierogis` means many images.

.. toctree::
   :maxdepth: 3
   :caption: usage

   cli
   ingredients
   examples
   kitchen

.. toctree::
   :maxdepth: 3
   :caption: api

   source/modules
