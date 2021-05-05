.. _threshold:

.. py:currentmodule:: pierogis.ingredients

threshold
~~~~~~~~~

*pixels included or excluded based on brightness*

.. code-block:: console

   $ pierogis threshold ./input.jpg -u 150 -l 20

.. figure:: https://media.githubusercontent.com/media/pierogis/pierogis/develop/demo/out/gnome_threshold.png
   :alt: thresholded gnome
   :align: center

   *very chill.*

By default, pixels with brightness outside of the thresholds provided become "included",
and pixels within the thresholds become "excluded" (greater than lower, but less than upper).
This can be flipped by providing the ``--inner`` flag.

By default, included means replaced with white, excluded with black.

:ref:`sort` uses this under the hood.

============================= =================================================== ============ =========
arg                           description                                         default      valid
============================= =================================================== ============ =========
``-l``, ``--lower-threshold`` pixels with intensity *below* this value are sorted ``64``       ``0-255``
``-u``, ``--upper-threshold`` pixels with intensity *above* this value are sorted ``180``      ``0-255``
``--inner``                   if provided, pixels between the threshold values    ``180``      flag
                              are included in the sort
``--include``                 hex color to substitute for white                   ``'ffffff'`` ``0-3``
``--exclude``                 hex color to substitute for black                   ``'000000'`` ``0-3``
============================= =================================================== ============ =========

See: :py:class:`~pierogis.kitchen.menu.threshold_filling.ThresholdFilling`, :py:class:`~threshold.Threshold`