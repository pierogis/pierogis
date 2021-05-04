.. _custom:

.. py:currentmodule:: pierogis.ingredients

custom
~~~~~~

*parse text for a recipe*

.. code-block:: console

   $ pierogis custom ./input.jpg "sort -u 100; quantize"
   $ # or
   $ pierogis custom ./input.jpg recipe.txt

*recipe.txt*

.. code-block:: text

   sort -u 100; quantize

.. figure:: https://media.githubusercontent.com/media/pierogis/pierogis/develop/demo/out/gnome_sort_quantize.png
   :alt: sorted and quantized gnome
   :align: center

   *very chill.*

.txt files and quoted strings can describe a series of fillings, piped from one to the next.

========== =========================================== ========== =====
arg        description                                 default    valid
========== =========================================== ========== =====
``recipe`` path to json or txt file to use as a recipe recipe.txt `str`
========== =========================================== ========== =====

See: :py:class:`~pierogis.kitchen.menu.custom_filling.CustomFilling`
