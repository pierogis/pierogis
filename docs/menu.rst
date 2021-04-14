menu
====

.. currentmodule:: pyrogis.ingredients

Here lie a bunch of commands for creating à la carte recipes and a command for combining several.

.. _resize:

resize
~~~~~~
*change the size of an image with options to maintain aspect ratio*

.. code-block:: console

   $ pyrogis resize ./input.jpg --scale .25
   $ pyrogis resize ./input.jpg --scale 4

   $ # or using exact dimension (aspect ratio maintained)
   $ pyrogis resize ./input.jpg --height 200
   $ pyrogis resize ./input.jpg --height 800

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

When used in a :ref:`custom` recipe, scaling down at the beginning of a recipe
and up at the end can lead to cool (and faster) results.

===================== ===================================== ============= =======
arg                   description                           default       valid
===================== ===================================== ============= =======
``--width``           width to resize to                    ``None``      ``str``
``--height``          height to resize to                   ``None``      ``str``
``--scale``           scale multiplier for width and height ``1``         ``str``
``--resample-filter`` a filter to be used with resizing     ``'nearest'`` ``str``
===================== ===================================== ============= =======

See: :py:class:`~pyrogis.kitchen.menu.resize_filling.ResizeFilling`

.. _quantize:

quantize
~~~~~~~~

*quantize an image to a smaller set of colors*

.. code-block:: console

   $ pyrogis quantize input.jpg -c aaaaaa 43ad32 696969 --repeats 3 --iterations 3
   $ # or
   $ pyrogis quantize input.jpg -n 16 --repeats 3 --iterations 3

.. figure:: https://media.githubusercontent.com/media/pierogis/pierogis/develop/demo/out/gnome_magic.png
   :alt: quantized gnome
   :align: center

   *very chill.*

Wraps `rscolorq <https://github.com/okaneco/rscolorq>`_ in python through pyo3 using
:py:class:`~quantize.SpatialQuantize`. Thank you to the author of that package.

========================== ==================================================== ========= =========
arg                        description                                          default   valid
========================== ==================================================== ========= =========
``-c``, ``--colors``       hex colors to base palette on (palette size ignored) ``None``  ``int``
``-n``, ``--palette-size`` number of colors in the palette to cluster for       ``8``     ``int``
``--repeats``              number of times to repeat a temperature for DA       ``1``     ``int``
``--iterations``           number of times to iterate a coarseness level        ``1``     ``int``
``--initial-temp``         initial temp to use in DA for optimization           ``1``     ``float``
``--final-temp``           final temp to use in DA for optimization             ``0.001`` ``float``
``--dithering-level``      relative dithering level (use .5-1.5)                ``0.8``   ``float``
========================== ==================================================== ========= =========

See: :py:class:`~pyrogis.kitchen.menu.quantize_filling.QuantizeFilling`

.. _custom:

custom
~~~~~~

*parse text for a recipe*

.. code-block:: console

   $ pyrogis custom ./input.jpg "sort -u 100; quantize"
   $ # or
   $ pyrogis custom ./input.jpg recipe.txt

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

See: :py:class:`~pyrogis.kitchen.menu.custom_filling.CustomFilling`

.. _sort:

sort
~~~~
*sort pixels along an axis*

.. code-block:: console

   $ pyrogis sort ./input.jpg -l 50 -u 180 -t 1

.. figure:: https://media.githubusercontent.com/media/pierogis/pierogis/develop/demo/out/gnome_sort.png
   :alt: sorted gnome
   :align: center

   *very chill.*

Use ``-l`` and ``-u`` as lower and upper thresholds
where contiguous groups of pixels
with brightness outside of the thresholds are sorted.

Use ``-t`` to provide the number of the sort direction should rotate
where 0 turns sorts from bottom to top.

If only ``--lower-threshold`` is provided, ``--upper-threshold`` is set to 255.
If only ``--upper-threshold`` is provided, ``--lower-threshold`` is set to 0.

============================= =================================================== ========= =========
arg                           description                                         default   valid
============================= =================================================== ========= =========
``-l``, ``--lower-threshold`` pixels with intensity *below* this value are sorted ``64``    ``0-255``
``-u``, ``--upper-threshold`` pixels with intensity *above* this value are sorted ``180``   ``0-255``
``-t``, ``--turns``           number of clockwise turns from sorting              ``0``     ``0-3``
                              bottom to top
``--ccw``                     if provided, ``turns`` will be applied              ``False`` flag
                              counter-clockwise instead
============================= =================================================== ========= =========

See: :py:class:`~pyrogis.kitchen.menu.sort_filling.SortFilling`

.. _threshold:

threshold
~~~~~~~~~

*pixels included or excluded based on brightness*

.. code-block:: console

   $ pyrogis threshold ./input.jpg -u 150 -l 20

.. figure:: https://media.githubusercontent.com/media/pierogis/pierogis/develop/demo/out/gnome_threshold.png
   :alt: thresholded gnome
   :align: center

   *very chill.*

Pixels with brightness outside of the thresholds provided become "included".
Pixels within the thresholds become "excluded" (greater than lower, but less than upper).
By default, included means replaced with white, excluded with black.

:ref:`sort` uses this under the hood.

============================= =================================================== ============ =========
arg                           description                                         default      valid
============================= =================================================== ============ =========
``-l``, ``--lower-threshold`` pixels with intensity *below* this value are sorted ``64``       ``0-255``
``-u``, ``--upper-threshold`` pixels with intensity *above* this value are sorted ``180``      ``0-255``
``--include``                 hex color to substitute for white                   ``'ffffff'`` ``0-3``
``--exclude``                 hex color to substitute for black                   ``'000000'`` flag
============================= =================================================== ============ =========

See: :py:class:`~pyrogis.kitchen.menu.threshold_filling.ThresholdFilling`

.. _rotate:

rotate
~~~~~~
*rotate pixels a given amount of 90 degree turns*

.. code-block:: console

   $ pyrogis rotate ./input.jpg -t 1 --ccw

.. figure:: https://media.githubusercontent.com/media/pierogis/pierogis/develop/demo/out/gnome_rotate.png
   :alt: rotated gnome
   :align: center

   *very chill.*

Use ``-t`` to indicate the number of turns.
Use ``--ccw`` to turn counterclockwise instead.

:ref:`sort` uses this under the hood.

=================== ====================================== ========= =======
arg                 description                            default   valid
=================== ====================================== ========= =======
``-t``, ``--turns`` number of clockwise turns              ``1``     ``0-3``
``--ccw``           if provided, ``turns`` will be applied ``False`` flag
                    counter-clockwise instead
=================== ====================================== ========= =======

See: :py:class:`~pyrogis.kitchen.menu.rotate_filling.RotateFilling`

.. _crop:

crop
~~~~
*crop pixels with options to define a selection box*

.. code-block:: console

   $ pyrogis crop ./input.jpg -x 20 --height 400 --aspect 1 --origin c

.. figure:: https://media.githubusercontent.com/media/pierogis/pierogis/develop/demo/out/gnome_crop.png
   :alt: cropped gnome
   :align: center

   *very chill.*

The interface for cropping is based on defining a rectangular area to select out of the image.

``--width`` and ``--height`` will correspond to percentages of input width if they are decimals
(.5 meaning: spanning half of the input width).
1 does not mean 100% of the pixels, leave out height/width to do that!

You can provide ``-x`` and ``-y`` to define an offset from the origin at which the rectangle is pegged.
x=0, y=0 corresponds to the bottom left of the image.

``-x`` and ``-y`` will also correspond to percentages if they are decimals
(.5 meaning: halfway offset from origin to end of the image in that axis).

.. _origins:

You can provide a direction that will define the origin
and the direction of the selection

*origins*

- ``sw`` bottom left (default) -> top right
- ``se`` bottom right -> top left
- ``nw`` top left -> bottom right
- ``ne`` top right -> bottom left
- ``n`` top center -> bottom center
- ``s`` bottom center -> top center
- ``e`` center right -> center left
- ``w`` center left -> center right
- ``c`` center center -> outwards

``--aspect`` will crop the image to the given aspect ratio.
It achieves this in different ways depending on the other options provided.
- If neither ``--width`` or ``--height`` are provided,
it will preserve one dimension and reduce another so as to not increase in size. Same treatment as resize.
- If both ``--width`` and ``--height`` are provided, the ``--aspect`` is ignored.
- If one of ``--width`` or ``--height`` are provided, the ``--aspect`` is applied to the missing dimension.

Pixel coordinates within the rectangle but without the input image will be ignored.

See :py:class:`~pyrogis.ingredients.crop.Crop`
documentation for a table of examples and their generated rectangles' bottom left and top right coordinates.

============ ========================================================= ========= ====================
arg          description                                               default   valid
============ ========================================================= ========= ====================
``--origin`` origin location and opposing direction to crop toward     ``sw``    see *origins*
``-x``       x origin offset; decimal for relative to input width      ``0``     ``float``, ``int``
``-y``       x origin offset; decimal for relative to input height     ``0``     ``float``, ``int``
``--width``  width to capture; decimal for relative to input width     ``None``  ``float``, ``int``
``--height`` width to capture; decimal for relative to input height    ``None``  ``float``, ``int``
``--aspect`` aspect ratio; ignored if ``height`` and ``width`` present ``None``  ``float``
============ ========================================================= ========= ====================

See: :py:class:`~pyrogis.kitchen.menu.crop_filling.CropFilling`
