"""
<a name="ingredients"></a>
## ingredients

>*"`pierogis` is the name of the framework;*
>
>*`pyrogis` is the name of the python package and cli tool"*
>
>\- a wise man

```python
from pyrogis import Pierogi, SpatialQuantize, Sort, Threshold, Dish, Recipe
```

A processing factory, called an `Ingredient`,
has a `prep` method for receiving parameters,
and a `cook` method for operating
on a numpy array to produce a programmatic output.

These two methods are usually called implicitly,
`prep` on __init__ and `cook` obfuscated in the typical usage flow.
`prep` can be seen as parameterizing the manipulation
while `cook` applies it (to an array).

### pierogi

`Pierogi` is one of the simplest `Ingredient` types.
It stores pixels, usually loaded from an image.

`Pierogi` is unique in that the array it returns from its cook function
is not based on the input

```python
pierogi = Pierogi(file="/Users/kyle/Desktop/image.jpg")
pierogi = Pierogi(pixels=np.array(
    [[[0, 0, 0], [0, 0, 0]], [[255, 255, 255], [255, 255, 255]]]
)
```

### quantize

`Quantize` is another `Ingredient`.
When cooked, it will process an incoming numpy array and return an array
where every pixel has been quantized to the closest color in the `palette`.

There is also the `SpatialQuantize` variant which is used for the cli tool.

```python
palette = [
    [0, 0, 0],
    [127, 127, 127],
    [255, 255, 255]
]

quantize = Quantize(palette=palette)
quantized_pixels = quantize.cook(pierogi.pixels)
```

This should produce a pixel for pixel quantized version of the input array.

As you can see above, an `Pierogi` has a `pixels` member.
This is the internal numpy pixel array of that `Pierogi`
with shape `(width, height, 3)`.

Some other `Ingredient` types include: `Threshold`, `Flip`, and `Rotate`.

### recipe

A typical flow allows you to create a pipeline of `Ingredient` types
that sequentially apply their `cook` method on to
the previous array of pixels.

A pipeline in `pierogis` is called a `Recipe`. It is an `Ingredient` itself.

```python
recipe = Recipe(ingredients=[pierogi, quantize])
recipe.cook()

recipe = Recipe(ingredients=[quantize])
recipe.cook(pierogi.pixels)
```

The two will produce the same result. But there's a better way.

### dish

>*"get to the point already"*
>
>\- a wiser man

We could also use a `Dish` to serve this recipe.
This is the recommended way to use `Recipe`.

```python
dish = Dish(recipe=recipe, pierogis=[pierogi])
cooked_dish = dish.serve()
```

The recipe gets cooked sequentially for each pierogi in `pierogis`.
The output dish has `pierogis` member set with cooked pierogis.
The `save` method of `dish` can be used as well.

### seasoning

There is also a concept of seasonings.
They can be used to apply something like a mask
to other ingredients that affect the pixels they act on.

```python
sort = Sort()
seasoning = Threshold()

sort.season(seasoning)
```

`Threshold.cook` outputs a black and white array.
Now that `sort` is seasoned with the `Threshold`,
it will only sort pixels that have been "colored"
white by the `Threshold`

## extending

To create a custom `Ingredient` type,
it must subclass `Ingredient` and override the `cook` and `prep`
methods.

```python
class Custom(Ingredient):
    def prep(self, brighten: int, scale: int, **kwargs):
        self.brighten = brighten
        self.scale = scale
    def cook(self, pixels: np.ndarray):
        return (self.pixels + self.brighten) /*self.scale
```

### prep

*Override `prep` to parameterize your manipulation.*

This means any settings, constants,
or inputs that configure the new functionality.
Think about the `palette` used with
quantization.

```python
def prep(self, brighten: int, scale: int, *args, **kwargs):
    self.brighten = brighten
    self.scale = scale
```

### cook

*Override `cook` to perform the manipulation.*

This is the function that you acts on an input pixel grid.
More specifically, this function receives
a `(width, height, 3)` `ndarray`
and should return a 3d array that is also size 3 in the last dimension.

```python
def cook(self, pixels: np.ndarray):
    return (self.pixels + self.brighten) * self.scale
```

This function increases the r, g, and b of every pixel by `self.brighten`
then multiplies that sum for each by `self.scale`.

Numpy operations can be pretty fast if you can keep them vectorized.
This means try to avoid looping over the columns
and rows of an array.
"""

from .chef import Chef
from .ingredients import Dish
from .ingredients import Ingredient
from .ingredients import Pierogi
from .ingredients import Quantize
from .ingredients import Recipe
from .ingredients import Sort
from .ingredients import SpatialQuantize
from .ingredients import Threshold

__version__ = '0.2.0'

__all__ = [
    'Pierogi',
    'Dish',
    'Ingredient',
    'Recipe',
    'Pierogi',
    'Quantize',
    'SpatialQuantize',
    'Sort',
    'Threshold',
    'Chef'
]
