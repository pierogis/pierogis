ingredients
===========

.. py:currentmodule:: pyrogis.ingredients

.. code-block:: python

   from pyrogis.ingredients import Pierogi, SpatialQuantize, Sort, Threshold, Dish, Recipe...

A processing factory, called an :py:class:`~ingredient.Ingredient`,
has a :py:meth:`~ingredient.Ingredient.prep` method for receiving parameters,
and a :py:meth:`~ingredient.Ingredient.cook` method for operating
on a numpy array to produce a programmatic output.

These two methods are usually called implicitly,
``prep`` through :py:meth:`~ingredient.Ingredient`
and ``cook`` obfuscated in the typical usage flow.
``prep`` can be seen as parameterizing the manipulation
while ``cook`` applies it (to an array).

Here are some examples of :py:class:`~ingredient.Ingredient` subtypes.

pierogi
-------

:py:class:`~ingredient.Ingredient` is one of the simplest :py:class:`~ingredient.Ingredient` types.
It stores pixels, usually loaded from an image.

:py:class:`~pierogi.Pierogi` is unique in that the array it returns from its ``cook`` function
is not based on the input

.. code-block:: python

   pierogi = Pierogi(file="/Users/kyle/Desktop/image.jpg")
   pierogi = Pierogi(pixels=np.array(
       [[[0, 0, 0], [0, 0, 0]], [[255, 255, 255], [255, 255, 255]]]
   )

quantize
--------

:py:class:`~quantize.Quantize` is another :py:class:`~ingredient.Ingredient`.
When cooked, it will process an incoming numpy array and return an array
where every pixel has been quantized to the closest color in the ``palette``.

There is also the :py:class:`~quantize.SpatialQuantize` variant which is used by the cli tool.

.. code-block:: python

   palette = [
      [0, 0, 0],
      [127, 127, 127],
      [255, 255, 255]
   ]

   quantize = Quantize(palette=palette)
   quantized_pixels = quantize.cook(pierogi.pixels)

This should produce a pixel for pixel quantized version of the input array.

As you can see above, a :py:class:`~pierogi.Pierogi` has a ``pixels`` member.
This is the internal numpy pixel array of that `Pierogi`
with shape ``(width, height, 3)``.

Some other :py:class:`~ingredient.Ingredient` types include:
:py:class:`~threshold.Threshold`, :py:class:`~flip.Flip`, and :py:class:`~rotate.Rotate`.

recipe
------

A typical flow allows you to create a pipeline of :py:class:`~ingredient.Ingredient` types
that sequentially apply their ``cook`` method on to
the previous array of pixels.

A pipeline in ``pierogis`` is called a :py:class:`~recipe.Recipe`.
It is an :py:class:`~ingredient.Ingredient` itself.

.. code-block:: python

   recipe = Recipe(ingredients=[pierogi, quantize])
   recipe.cook()

   recipe = Recipe(ingredients=[quantize])
   recipe.cook(pierogi.pixels)

The two will produce the same result. But there's a better way.

dish
----

    *"get to the point already"*

    - a wiser man

We could also use a :py:class:`~dish.Dish` to serve this recipe.
This is the recommended way to use :py:class:`~recipe.Recipe`.

.. code-block:: python

   dish = Dish(recipe=recipe, pierogi=pierogi)
   cooked_dish = dish.serve()

The recipe gets cooked sequentially for each pierogi in ``pierogis``.
The output ``cooked_dish`` has ``pierogi`` member set with cooked pixels.

seasoning
~~~~~~~~~

There is also a concept of seasonings.
They can be used to apply something like a mask
to other ingredients that affect the pixels they act on.

.. code-block:: python

   sort = Sort()
   threshold = Threshold()

   # season sort with threshold
   sort.season(threshold)

:py:meth:`~threshold.Threshold.cook` outputs a black and white array.
Now that ``sort`` is seasoned with the ``Threshold``,
it will only sort pixels that have been "colored"
white by the ``Threshold``.

extending
~~~~~~~~~

To create a custom :py:class:`~ingredient.Ingredient` type,
it must subclass ``Ingredient`` and override the
:py:meth:`~ingredient.Ingredient.cook` and :py:meth:`~ingredient.Ingredient.prep` methods.

.. code-block:: python

   class Custom(Ingredient):
       def prep(self, brighten: int, scale: int, **kwargs):
           self.brighten = brighten
           self.scale = scale
       def cook(self, pixels: np.ndarray):
           return (self.pixels + self.brighten) /*self.scale

prep
----

*Override to parameterize your manipulation*

This means any settings, constants,
or inputs that configure the new functionality.
Think about the ``palette`` used with
quantization.

.. code-block:: python

   def prep(self, brighten: int, scale: int, *args, **kwargs):
       self.brighten = brighten
       self.scale = scale

cook
----

*Override to perform the manipulation*

This is the function that you acts on an input pixel grid.
More specifically, this function receives
a ``(width, height, 3)`` ``ndarray``
and should return a 3d array that is also size 3 in the last dimension.

.. code-block:: python

   def cook(self, pixels: np.ndarray):
       return (self.pixels + self.brighten) * self.scale

This function increases the r, g, and b of every pixel by ``self.brighten``
then multiplies that sum for each by ``self.scale``.

Numpy operations can be pretty fast if you can keep them vectorized.
This means try to avoid looping over the columns
and rows of an array.