# pierogis

### Image processing with numpy

This library uses image processing factories to create rendering pipelines.

## Install

Install with pip

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

`Pierogi` is one of the simplest `Ingredient`s. It just loads an image when `cook`ed.
```python
from pierogis import Pierogi

pierogi = Pierogi()
pierogi.prep(file="/Users/kyle/Desktop/image.jpg")

pierogi.cook()
pierogi.show()
```

```python
palette = [
    [0, 0, 0],
    [127, 127, 127],
    [255, 255, 255]
]

quantize = Quantize()
quantize.prep(palette)
```

Some `Ingredient` examples include: `Threshold`, `Mix`, and `Quantize`.

A typical flow allows you to create a pipeline of `Ingredients` that sequentially apply their `cook` method on to the
previous array of pixels
