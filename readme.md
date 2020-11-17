# pierogis

### Image processing with numpy

This library uses image processing factories to create rendering pipelines.

A factory, called an `Ingredient`, has a `prep` method for receiving parameters, and a `cook` method for operating
on a numpy array to produce a programmatic output.

Some `Ingredient` examples include: `Threshold`, `Mix`, and `Quantize`.

### Features
##### Lazy Rendering
A typical flow allows you to create a pipeline of `Ingredients` that sequentially apply their `cook` method on to the
previous array of pixels

##### Customizable
Easy to create custom `Ingredients`