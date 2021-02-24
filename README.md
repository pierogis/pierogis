# pierogis

**image processing framework**

`pierogis` is a framework for image processing. Ingredients that describe image processing functions can be assembled
into recipes and cooked.

`pyrogis` is a python library and cli tool implementing this framework.

```bash
pip install pyrogis
pyrogis chef teton.png "resize --width 768 --height 768; sort; quantize; resize --scale 4" -o output.png
# or
pyrogis chef teton.png recipe.txt -o output.png
```

*recipe.txt*
```text
resize --width 768 --height 768;
sort;
quantize -c 000000 ffffff 668a61 cbb8a2 b6d655 434d1f 5fb7d2 6d8ab9 3876c1 515b5e a8725f d7b6aa 3c2329 f78693 637186 00407A;
resize -s 4;
```

![sorted and quantized teton](https://raw.githubusercontent.com/pierogis/pierogis/develop/demo/out/teton.png)

- [install](#install)
- [features](#features)
- [cli](#cli)
- [package](#package)
- [acknowledgements](#acknowledgements)
- [issues and contributing](#issues-and-contributing)

<a name="install"></a>

## install

**install from a wheel with pip**

```sh
pip install pyrogis
```

Depends on `numpy` and `PIL`. PIL requires some external C libraries for handling image files. You probably don't have
to worry about this. If you do, try a `conda` installation.

To build from source (either the repository or the sdist), you will need to install the rust stable toolchain
and `setuptools-rust`.

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
pip install setuptools-rust

pip install .
```

<a name="features"></a>

## features

- **CLI** - Use the CLI to cook à la carte recipes, or provide a recipe in a document
- **Animations** - Animations (gifs and movies) can be cooked in one command
- **Extendable** - Easy to create custom manipulations (see [package](#package))
- **Lazy Rendering** - Render a manipulation after constructing your pipeline (see [package](#package))
- **Numpy or Rust backend** - Image processing functions use Numpy for (python relative) fast operations. Some
  ingredients use compiled `Rust` for more speed.

# usage

<a name="cli"></a>

## cli

All of the cli commands look like this.

```bash
pyrogis {order} {path} [-o output] [... order options] [--frames] [--fps fps] [--duration duration] [--no-optimize]
```

`order` is one of

- [`chef`](#chef)
- [`sort`](#sort)
- [`quantize`](#quantize)
- [`threshold`](#threshold)
- [`resize`](#resize)
- [`plate`](#plate)

The following options are used for each `order` ([`sort`](#sort), [`quantize`](#quantize), etc.).
A directory can be used for `path`, in which case the program will try to cook each file in the directory.
If an `output` filename or dir is provided, it should match the expected output.

In addition, each `order` or "menu item" has its own set of options.

|arg|description|default|valid|
|:----:|-----------|:-----:|:---:|
|`order`|order type / menu item to cook|`required`|sort, quantize, chef, threshold, plate, resize|
|`path`|path to input media|`required`|`dir`, `image`, `animation`|
|`-o`,`--output`|name of the output directory or file|depends on output type|`str`|
|`--frames`|if present, frames will be cooked but not assembled into animation (`output` is treated as dir)|False|flag|
|`--fps`|fps to output an animation at (ignored if single frame)|25|`int`|
|`--duration`|ms frame duration to output an animation with (ignored if single frame, overrides duration)|`None`|`int`|
|`--no-optimize`|if present and output would be .gif, the gif is not optimized using pygifsicle|`False`|`int`|

If the input file is a directory or a movie file (anything animated),
the output will be an animation as well. Artifact "cooked" folder will contain frames.
If you don't understand what output type to expect from your command, don't provide `output`.

### sort

*sort pixels along an axis*

```bash
pyrogis sort ./input.jpg -l 50 -u 180 -t 1
```

Use `-l` and `-u` as lower and upper thresholds
where contiguous groups of pixels
with brightness outside of the thresholds are sorted.

If only lower is provided, upper is set to 255.
If only upper is provided, lower is set to 0.

![sorted gnome](https://raw.githubusercontent.com/pierogis/pierogis/develop/demo/out/gnome_sort.png)

|arg|description|default|valid|
|------|-----------|:-----:|:---:|
|`-l`, `--lower-threshold`|pixels with intensity *below* this value are sorted|`64`|`0-255`|
|`-u`, `--upper-threshold`|pixels with intensity *above* this value are sorted|`180`|`0-255`|
|`-t`, `--turns`|number of clockwise turns from sorting bottom to top|`0`|`0-3`|
|`--ccw`|if provided, `turns` will be applied counter-clockwise|False|flag|

### quantize

*quantize an image to a smaller set of colors*

![quantized gnome](https://raw.githubusercontent.com/pierogis/pierogis/develop/demo/out/gnome_magic.png)

```bash
pyrogis quantize input.jpg -c aaaaaa 43ad32 696969 --repeats 3 --iterations 3
# or
pyrogis quantize input.jpg -n 16 --repeats 3 --iterations 3
```

Wraps [`rscolorq`](https://github.com/okaneco/rscolorq)) in python.
Thank you to the author of that package.

|arg|description|default|valid|
|:----:|-----------|:-----:|:---:|
|`-c`, `--colors`|hex colors to base palette on (palette size ignored)|`None`|`int`|
|`-n`, `--palette_size`|number of colors in the palette to cluster for|8|`int`|
|`--repeats`|number of times to repeat a temperature for DA|1|`int`|
|`--iterations`|number of times to repeat an iteration of a coarseness level|1|`int`|
|`--initial-temp`|initial temp to use in DA for optimization|1|`float`|
|`--final-temp`|final temp to use in DA for optimization|0.001|`float`|
|`--dithering-level`|relative dithering level (use .5-1.5)|0.8|`float`|

### chef

*parse text for a recipe*

![sorted and quantized gnome](https://raw.githubusercontent.com/pierogis/pierogis/develop/demo/out/gnome_sort_quantize.png)

.txt files and quoted strings can describe a series of CLI recipes, piped from one to the next.

```bash
pyrogis chef ./input.jpg "sort -u 100; quantize"
# or
pyrogis chef ./input.jpg recipe.txt
```

*recipe.txt*
```text
sort -u 100; quantize
```

|arg|description|default|valid|
|:----:|-----------|:-----:|:---:|
|recipe|path to json or txt file to use as a recipe|recipe.txt|`str`|

### threshold

*pixels included or excluded based on brightness*

![threshold gnome](https://raw.githubusercontent.com/pierogis/pierogis/develop/demo/out/gnome_threshold.png)

Pixels with brightness outside of the thresholds provided become "included".
Pixels within the thresholds become "excluded" (greater than lower, but less than upper).
By default, included means replaced with white, excluded with black.

`sort` uses this under the hood.

```bash
pyrogis threshold ./input.jpg -u 150 -l 20 
```

|arg|description|default|valid|
|:----:|-----------|:-----:|:---:|
|`-u`,`--upper-threshold`|pixels above this value are white|180|`int`|
|`-l`,`--lower-threshold`|pixels below this value are white|64|`int`|
|`--include`|hex color to substitute for white|ffffff|`str`|
|`--exclude`|hex color to substitute for black|000000|`str`|

### resize

*change the size of an image with options to maintain aspect ratio*

Provide one of `width` or `height` and the other will scale appropriately. Use of both `height` and `width` is probably
redundant and will stretch the image if the ratio is not the same.

`scale` can also be provided as an alternative or alongside `height`/`width`.

By default, a nearest neighbor scaling "filter" is used. When scaling up, nearest neighbor preserves the pixelated look
if `scale` is a whole number
(or `width`/`height` are provided as multiples of the current size).

See [PIL documentation](https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-filters)
on filters

When used in a `chef` recipe, scaling down at the beginning of a recipe and up at the end can lead to cool (and faster)
results.

```bash
pyrogis resize ./input.jpg -s .25
pyrogis resize ./input.jpg -s 4

# or using exact dimension (aspect ratio maintained)
pyrogis resize ./input.jpg -h 200
pyrogis resize ./input.jpg -h 800
```

|arg|description|default|valid|
|:----:|-----------|:-----:|:---:|
|`--width`|width to resize to|`None`|`int`|
|`--height`|height to resize to|`None`|`int`|
|`--scale`|scale multiplier for width and height|1|`float`|
|`--filter`|a filter to be used with resizing|nearest|nearest, bicubic, bilinear, box, hamming, lanczos|

### plate

*bundle a directory of frames into an animation*

When `--frames` flag is present for a cook operation on an animation file (gif, mp4, etc.), the output is left in a
directory and not compiled into a movie file.

`plate` can be used to take this input directory and compile into a movie file.

Doesn't work as an ingredient in `chef` `recipe`.

`duration` will override `fps`.

The options for this can be provided to any `order` if the output would be an animation.

```bash
pyrogis plate ./cooked --fps 50
```

|arg|description|default|valid|
|:----:|-----------|:-----:|:---:|
|`--fps`|fps to output an animation at (ignored if single frame)|25|`int`|
|`--duration`|ms frame duration to output an animation with (ignored if single frame, overrides duration)|`None`|`int`|
|`--no-optimize`|if present and output would be .gif, the gif is not optimized using pygifsicle|`False`|`int`|

<a name="package"></a>

## package

> *"`pierogis` is the name of the framework;*
>
>*`pyrogis` is the name of the python package and cli tool"*
>
>\- a wise man

```python
import pyrogis
```

[Docs](https://pierogis.github.io/pierogis/pyrogis.html) are automatically generated by [pdoc](https://pdoc.dev)

The created files can be found in this repository in the `docs` folder

<a name="acknowledgements"></a>

## acknowledgements

The original python [pixelsort](https://github.com/satyarth/pixelsort) package inspired this package. While the
underlying [algorithm](https://github.com/kimasendorf/ASDFPixelSort) of that package and of `sort` in this one is
supposed to be functionally the same, details of the implementation may differ, and it makes up just part of this
package.

The quantizing algorithm used in this package is implemented by [`rscolorq`](https://github.com/okaneco/rscolorq), which
is a port of [`scolorq`](http://people.eecs.berkeley.edu/~dcoetzee/downloads/scolorq/), itself an implementation of
Spatial Color Quantization.

<a name="issues-and-contributing"></a>

## issues and contributing

When you encounter an error, there are some guidelines that will make it easier to help you:

- Ensure that you are using the latest version of the package. It's early days so errors and updates will be frequent.
  Use `pip uninstall pyrogis` then `pip install pyrogis --no-cache-dir` to reinstall.
- Provide the version of `pyrogis` that you are using in issues to rule that out.
  `pip list` -> pyrogis \_.\_.\_
- Provide the traceback or error message if you can.
- Provide your os and any other specific information relevant to how you are trying to use the package.
- Provide the code or the cli command that triggered the error.
- If the problem is visual: that can be more difficult to debug. Try to use an image hosting site if you want to share
  what you are seeing in an issue.
- If you are getting different behavior than you expect: that could be an error or a feature too.
- If your problem is with installation: try conda, preinstall `numpy` and `pillow`, install the rust toolchain, and
  start praying. There will be a website with a visual editor for this software so stay tuned.

Hopefully all levels of skills can use this package. Any form of contributing is appreciated; passive-aggressive
semi-anonymous thumbs down is not appreciated.

Everyone using and contributing to this package is doing it for the love of the game.

Don't feel like your issue is too small to make an issue. Pull requests are always welcome and anyone interested in dev
work should join the
[discord](https://discord.gg/9XpEjMw3Rx).

`Ingredient` type algorithm/function suggestions can go in the ingredients channel. You can post your creations in the
demo channel as well.