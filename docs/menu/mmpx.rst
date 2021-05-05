.. _mmpx:

.. py:currentmodule:: pierogis.ingredients

mmpx
~~~~
*2x image scaling*

.. code-block:: console

   $ pierogis custom ./input.jpg "resize -s .5; quantize; mmpx"

.. figure:: https://media.githubusercontent.com/media/pierogis/pierogis/develop/demo/out/gnome_mmpx.png
   :alt: mmpxed gnome
   :align: center

   *very chill.*

Results in an image with size 2 x width and 2 x height using :py:class:`~mmpx.MMPX`.
This algorithm uses a series of rules based on nearby pixels to determine how to map
a single pixel to 4 corresponding (2*2) output pixels.

You can read about the
`algorithm <https://casual-effects.com/research/McGuire2021PixelArt/index.html>`_,
and check out its
`implementation <https://github.com/pierogis/mmpx-rs>`_
done in Rust (like :ref:`quantize`).

Thank you to the authors of that algorithm, it's very cool and performant.

A recipe with ``resize -s .5``, a "style" ingredient/filling (``quantize`` for example), then ``mmpx`` creates a nice effect.
This is because MMPX is designed for pixel art (small color palette and large pixels),
meaning pixels in normal images will typically be scaled using nearest neighbor.

There are no options specific to this ingredient/filling.

See: :py:class:`~pierogis.kitchen.menu.mmpx_filling.MMPXFilling`
