# pierogis

**Image processing with numpy**

This library uses image processing factories to create rendering pipelines.

## Install

**Install from source with pip**

```sh
pip install .
```

Depends on `numpy` and `PIL`. PIL requires some external C libraries for handling image files. You probably don't have
to worry about this.

## Features

- **Lazy Rendering** - Render a manipulation after constructing your pipeline
- **Extendable** - Easy to create custom manipulations

## Usage
A factory, called an `Ingredient`, has a `prep` method for receiving parameters, and a `cook` method for operating on a
numpy array to produce a programmatic output.

These two methods are usually called implicitly, `prep` on init and `cook` when rendering.
`prep` can be seen as parameterizing the manipulation while `cook` applies it (to an array).

#### Images

`Pierogi` is one of the simplest `Ingredient` types. It just loads its reference image.
```python
pierogi = Pierogi(file="/Users/kyle/Desktop/image.jpg")
```
#### Manipulations

`Quantize` is another `Ingredient`. When cooked, one will process an incoming numpy array and return an array where every pixel has been quantized to the closest color in the `palette`.

Note how it is less static than a `Pierogi`, almost *precooked*. When a pierogi is cooked, the "manipulation" that it applies is just loading the picture on top.
Quantize, like many other `Ingredient` types, depends on a meaningful input to `cook` to produce a meaningful output

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

As you can see above, an `Ingredient` has a `pixels` member. This is the internal numpy pixel array of that `Ingredient`.
Its shape is (width, height, 3).

Also consider how `quantize.pixels` doesn't really make sense compared to `pierogi.pixels`.
This is related to the relative staticness of the `Pierogi`. More on that later.

Some other `Ingredient` types include: `Threshold`, `Sort`, and `Recipe`.

#### Pipelines

A typical flow allows you to create a pipeline of `Ingredients` that sequentially apply their `cook` method on to the
previous array of pixels

A pipeline in `pierogis` is called a `Recipe`. It is an `Ingredient` itself.

```python
recipe = Recipe(ingredients=[pierogi, quantize])
# recipe.cook(...) 
# we could input a base pixel array to go beneath pierogi

# or use a dish to serve this recipe
dish = Dish(recipe=recipe)
dish.serve()
```

The recipe gets cooked sequentially, then the final output of that is set to dish.pixels.
This dish could be used like a pierogi now, *precooked*.

#### Seasoning

## Extending

If you want to create your own `Ingredient` type, you must subclass `Ingredient` and override the `cook` and `prep` methods.

#### prep

Use `prep` to parameterize your manipulation.

This means any settings, constants, or inputs that configure the new functionality.
Think about the `palette` used with quantization.

```python
def prep(self, brighten: int, scale: int, *args, **kwargs):
    self.brighten = brighten
    self.scale = scale
```

#### cook

Use `cook` to perform the manipulation.

This is the function that you are applying to each pixel.
More specifically, this function has a (width, height, 3) `ndarray` and should return a 3d array that is also size 3 in the last dimension.

```python
def cook(self, pixels: np.ndarray):
    return (self.pixels + self.brighten) / self.scale
```

This function increases the r, g, and b of every pixel by `self.brighten`
then divides them each by `self.scale`.

Numpy operations can be pretty fast if you can keep them vectorized.
This means try to avoid looping over the columns and rows of an array.