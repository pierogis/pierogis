.. _sort:

.. py:currentmodule:: pyrogis.ingredients

sort
~~~~
*sort pixels along an axis*

.. code-block:: console

   $ pyrogis sort ./input.jpg -l 50 -u 180 --inner -t 1

.. figure:: https://media.githubusercontent.com/media/pierogis/pierogis/develop/demo/out/gnome_sort.png
   :alt: sorted gnome
   :align: center

   *very chill.*

Use ``-l`` and ``-u`` as lower and upper thresholds
where contiguous groups of pixels
with brightness outside of the thresholds are sorted.
Providing ``--inner`` sorts values between these thresholds.
See :ref:`threshold`.

Use ``-t``, ``-a``, ``--clockwise``, ``resample-filter`` to describe the direction of the sort.
See :ref:`rotate`.

If only ``--lower-threshold`` is provided, ``--upper-threshold`` is set to 255.
If only ``--upper-threshold`` is provided, ``--lower-threshold`` is set to 0.

============================= =================================================== ============= =========
arg                           description                                         default       valid
============================= =================================================== ============= =========
``-l``, ``--lower-threshold`` pixels with intensity *<=* this value are sorted    ``64``        ``0-255``
``-u``, ``--upper-threshold`` pixels with intensity *>=* this value are sorted    ``180``       ``0-255``
``--inner``                   if provided, pixels between (inclusive) the
                              threshold values are included in the sort           ``False``     ``0-255``
``-t``, ``--turns``           number of clockwise turns from sorting              ``0``         ``0-3``
                              bottom to top
``-a``, ``--angle``           degrees to rotate through each turn                 ``90``        ``int``
``--ccw``                     if provided, ``turns`` will be applied              ``False``     flag
                              counter-clockwise instead
``--resample-filter``         a filter to be used with rotating                   ``'nearest'`` ``str``
============================= =================================================== ============= =========

See: :py:class:`~pyrogis.kitchen.menu.sort_filling.SortFilling`,
:py:class:`~pyrogis.kitchen.menu.rotate_filling.RotateFilling`,
:py:class:`~pyrogis.kitchen.menu.threshold_filling.ThresholdFilling`
