.. _threshold:

.. currentmodule:: pyrogis.ingredients

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