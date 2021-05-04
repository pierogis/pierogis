.. _resize:

.. py:currentmodule:: pierogis.ingredients

resize
~~~~~~
*change the size of an image with options to maintain aspect ratio*

.. code-block:: console

   $ pierogis resize ./input.jpg --scale .25
   $ pierogis resize ./input.jpg --scale 4

   $ # or using exact dimension (aspect ratio maintained)
   $ pierogis resize ./input.jpg --height 200
   $ pierogis resize ./input.jpg --height 800

.. figure:: https://media.githubusercontent.com/media/pierogis/pierogis/develop/demo/out/gnome_resize.png
   :alt: resized gnome
   :align: center

   *very chill.*

Provide one of ``--width`` or ``--height`` and the other will scale appropriately.
Use of both ``--height`` and ``width`` is probably redundant
and will stretch the image if the ratio is not the same.

``--scale`` can also be provided as an alternative or alongside ``--height``/``--width``.

By default, a nearest neighbor scaling "filter" is used.
When scaling up, nearest neighbor preserves the pixelated look
if ``--scale`` is a whole number
(or ``--width``/``--height`` are provided as multiples of the current size).

See `PIL documentation <https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-filters>`_
on filters.

.. code-block:: python

   choices = {
       'default': Image.NEAREST,
       'nearest': Image.NEAREST,
       'box': Image.BOX,
       'bicubic': Image.BICUBIC,
       'bilinear': Image.BILINEAR,
       'hamming': Image.HAMMING,
       'lanczos': Image.LANCZOS,
   }

When used in a :ref:`custom` recipe, scaling down at the beginning of a recipe
and up at the end can lead to cool (and faster) results.

===================== ===================================== ============= =====================
arg                   description                           default       valid
===================== ===================================== ============= =====================
``--width``           width to resize to                    ``None``      ``str``
``--height``          height to resize to                   ``None``      ``str``
``--scale``           scale multiplier for width and height ``1``         ``str``
``--resample-filter`` a filter to be used with resizing     ``'nearest'`` see ``choices`` above
===================== ===================================== ============= =====================

See: :py:class:`~pierogis.kitchen.menu.resize_filling.ResizeFilling`
