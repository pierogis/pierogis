.. _crop:

.. py:currentmodule:: pierogis.ingredients

crop
~~~~
*crop pixels by defining a selection box*

.. code-block:: console

   $ pierogis crop ./input.jpg -x 20 --height 400 --aspect 1 --origin c

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

- If neither ``--width`` nor ``--height`` are provided, it will preserve one dimension and reduce another so as to not increase in size. Same treatment as resize.
- If both ``--width`` and ``--height`` are provided, the ``--aspect`` is ignored.
- If one of ``--width`` or ``--height`` are provided, the ``--aspect`` is applied to the missing dimension.

Pixel coordinates within the rectangle but without the input image will be ignored.


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

The following table explains the x,y coordinates (the last 4 columns)
of the cropped output's bottom left and top right corners for each set of inputs.

0,0 corresponds to the left,bottom of an image
and a larger x,y coordinate indicates toward the right,top of the image.
If you are reading this you are a champion.

.. csv-table:: Crop Examples
   :file: crop_table.csv
   :header-rows: 1

See: :py:class:`~pierogis.kitchen.menu.crop_filling.CropFilling`, :py:class:`~crop.Crop`
