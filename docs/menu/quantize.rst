.. _quantize:

.. py:currentmodule:: pierogis.ingredients

quantize
~~~~~~~~

*quantize an image to a smaller set of colors*

.. code-block:: console

   $ pierogis quantize input.jpg -c aaaaaa 43ad32 696969 --repeats 3 --iterations 3
   $ # or
   $ pierogis quantize input.jpg -n 16 --repeats 3 --iterations 3

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

See: :py:class:`~pierogis.kitchen.menu.quantize_filling.QuantizeFilling`
