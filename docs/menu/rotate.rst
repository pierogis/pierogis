.. _rotate:

.. currentmodule:: pyrogis.ingredients

rotate
~~~~~~
*rotate pixels a given amount of 90 degree turns*

.. code-block:: console

   $ pyrogis rotate ./input.jpg -t 1 --ccw

.. figure:: https://media.githubusercontent.com/media/pierogis/pierogis/develop/demo/out/gnome_rotate.png
   :alt: rotated gnome
   :align: center

   *very chill.*

Use ``-t`` to indicate the number of turns (defaults to 1).

Use ``-a`` to indicate the degree magnitude of each turn (defaults to 90).

Use ``--ccw`` to turn counterclockwise instead.

Use ``--resample-filter`` to define a PIL resample filter (defaults to nearest neighbor).

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


:ref:`sort` uses this under the hood.

===================== ====================================== ============= =======
arg                   description                            default       valid
===================== ====================================== ============= =======
``-t``, ``--turns``   number of clockwise turns              ``1``         ``0-3``
``-a``, ``--angle``   degrees to rotate through each turn    ``90``        ``int``
``--ccw``             if provided, ``turns`` will be applied ``False``     flag
                      counter-clockwise instead
``--resample-filter`` a filter to be used with resizing      ``'nearest'`` ``str``
===================== ====================================== ============= =======

See: :py:class:`~pyrogis.kitchen.menu.rotate_filling.RotateFilling`