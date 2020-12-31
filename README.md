# pierogis

**image processing with numpy**

This library uses image processing factories to create rendering pipelines.

## install

**Install from source with pip**

```sh
pip install pierogis
```

Depends on `numpy` and `PIL`. PIL requires some external C libraries for handling image files. You probably don't have
to worry about this. If you do, try a `conda` installation.

### features

- **Lazy Rendering** - Render a manipulation after constructing your pipeline
- **Extendable** - Easy to create custom manipulations
- **CLI** - Use the CLI to cook à la carte recipes, or provide a recipe in a document

# usage

## cli

```bash
pierogis {recipe} -o output.png path
```

These options are part of each recipe subcommand (`sort`, `quantize`, etc.).

|arg|description|default|valid|
|:----:|-----------|:-----:|:---:|
|`recipe`|provide the recipe to cook|`10`|`sort`, `quantize`, `chef`|

### sort

```bash
pierogis sort ./input.jpg -o output.png -l 50 -u 180 -t 1
```

|arg|description|default|valid|
|------|-----------|:-----:|:---:|
|`-l`, `--lower-threshold`|pixels with intensity *below* this value serve as sort boundaries|`64`|`0-255`|
|`-u`, `--upper-threshold`|pixels with intensity *above* this value serve as sort boundaries|`180`|`0-255`|
|`-t`, `--turns`|number of turns|`0`|`0-3`|

### quantize

Quantize an image to a set of colors.

```bash
pierogis quantize ./input.jpg -o output.png -k 10
```

|arg|description|default|valid|
|:----:|-----------|:-----:|:---:|
|-k|number of colors in the palette to cluster for|`10`|`int`|

### chef

Parse a file for a recipe.

Json files can describe a dish, and txt files can describe a series of CLI recipes, piped from one to the next. See xx
for guidance on how to provide a dish in json.

```bash
pierogis chef ./input.jpg recipe.json -o output.png
```

|arg|description|default|valid|
|:----:|-----------|:-----:|:---:|
|recipe|path to json or txt file to use as a recipe|`recipe.json`, `recipe.txt`|`str`|

## package

A factory, called an `Ingredient`, has a `prep` method for receiving parameters, and a `cook` method for operating on a
numpy array to produce a programmatic output.

These two methods are usually called implicitly, `prep` on init and `cook` when rendering.
`prep` can be seen as parameterizing the manipulation while `cook` applies it (to an array).

### pierogi

`Pierogi` is one of the simplest `Ingredient` types. It just loads its reference image.

```python
pierogi = Pierogi(file="/Users/kyle/Desktop/image.jpg")
```

### quantize

`Quantize` is another `Ingredient`. When cooked, it will process an incoming numpy array and return an array where every
pixel has been quantized to the closest color in the `palette`.

Note how it is less static than a `Pierogi`, almost *precooked*. When a pierogi is cooked, the "manipulation" that it
applies is just loading the picture on top. Quantize, like many other `Ingredient` types, depends on a meaningful input
to `cook` to produce a meaningful output

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

As you can see above, an `Ingredient` has a `pixels` member. This is the internal numpy pixel array of that `Ingredient`
with shape `(width, height, 3)`.

Also consider how `quantize.pixels` doesn't really make sense compared to `pierogi.pixels`. This is related to the
relative staticness of the `Pierogi`. More on that later.

Some other `Ingredient` types include: `Threshold`, `Flip`, and `Rotate`.

### recipe

A typical flow allows you to create a pipeline of `Ingredients` that sequentially apply their `cook` method on to the
previous array of pixels.

A pipeline in `pierogis` is called a `Recipe`. It is an `Ingredient` itself.

```python
recipe = Recipe(ingredients=[pierogi, quantize])
recipe.cook()

recipe = Recipe(ingredients=[quantize])
recipe.cook(pierogi.pixels)
```

The will produce the same result.

### dish

We could also use a `Dish` to serve this recipe. This is the recommended way to use `Recipe`.

```python
dish = Dish(recipe=recipe)
ingredient = dish.serve()
```

The recipe gets cooked sequentially. The output ingredient can be used like a pierogi now, *precooked*.

### seasoning

## extending

If you want to create your own `Ingredient` type, you must subclass `Ingredient` and override the `cook` and `prep`
methods.

### prep

Use `prep` to parameterize your manipulation.

This means any settings, constants, or inputs that configure the new functionality. Think about the `palette` used with
quantization.

```python
def prep(self, brighten: int, scale: int, *args, **kwargs):
    self.brighten = brighten
    self.scale = scale
```

### cook

Use `cook` to perform the manipulation.

This is the function that you are applying to each pixel. More specifically, this function has
a `(width, height, 3)` `ndarray`
and should return a 3d array that is also size 3 in the last dimension.

```python
def cook(self, pixels: np.ndarray):
    return (self.pixels + self.brighten) / self.scale
```

This function increases the r, g, and b of every pixel by `self.brighten`
then divides them each by `self.scale`.

Numpy operations can be pretty fast if you can keep them vectorized. This means try to avoid looping over the columns
and rows of an array.

## acknowledgements

The original python [pixelsort](https://github.com/satyarth/pixelsort) package inspired this package. While the
underlying [algorithm](https://github.com/kimasendorf/ASDFPixelSort) of that package and of `sort` in this one is
supposed to be functionally the same, details of the implementation differ, and it makes up just part of this package.
