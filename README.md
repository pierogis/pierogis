# pierogis

**image processing framework**

`pierogis` is a framework for image processing.
Ingredients that describe image processing functions can be assembled
into recipes and cooked.

`pyrogis` is a python library and cli tool implementing this framework.

```bash
pip install pyrogis
pyrogis chef input.png "sort; quantize" -o output.png
```

![sorted and quantized gnome](https://raw.githubusercontent.com/pierogis/pierogis/master/demo/out/gnome_sort_quantize.png)

- [install](#install)   
- [features](#features)   
- [issues and contributing](#issues-and-contributing)   
- [cli](#cli)   
- [package](#package)
- [acknowledgements](#acknowledgements)

<a name="install"></a>
## install

**install from a wheel with pip**

```sh
pip install pyrogis
```

Depends on `numpy` and `PIL`. PIL requires some external C libraries for handling image files.
You probably don't have to worry about this. If you do, try a `conda` installation.

To build from source (either the repository or the sdist), you will need to install the rust stable toolchain and `setuptools-rust`.
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
pip install setuptools-rust

pip install .
```

<a name="features"></a>
## features

- **Lazy Rendering** - Render a manipulation after constructing your pipeline
- **Extendable** - Easy to create custom manipulations
- **CLI** - Use the CLI to cook à la carte recipes, or provide a recipe in a document
- **Numpy or Rust backend** - Image processing functions use Numpy for (python relative) fast operations.
Some ingredients use compiled `Rust` for more speed.

<a name="issues-and-contributing"></a>
## issues and contributing

When you encounter an error, there are some guidelines that will make it easier to help you:
- Ensure that you are using the latest version of the package.
  It's early days so errors and updates will be frequent.
  Use `pip uninstall pyrogis` then `pip install pyrogis --no-cache-dir` to reinstall.
- Provide the version of `pyrogis` that you are using in issues to rule that out.
  `pip list` -> pyrogis \_.\_.\_
- Provide the traceback or error message if you can.
- Provide your os and any other specific information relevant to how you are trying to use the package.
- Provide the code or the cli command that triggered the error.
- If the problem is visual: that can be more difficult to debug.
  Try to use an image hosting site if you want to share what you are seeing in an issue.
- If you are getting different behavior than you expect: that could be an error or a feature too.
- If your problem is with installation: try conda, preinstall `numpy` and `pillow`,
  install the rust toolchain, and start praying.
  There will be a website with a visual editor for this software so stay tuned.

Hopefully all levels of skills can use this package.
Any form of contributing is appreciated;
passive-aggressive semi-anonymous thumbs down is not appreciated.

Everyone using and contributing to this package
is doing it for the love of the game.

Don't feel like your issue is too small to make an issue.
Pull requests are always welcome and anyone interested in dev work should join the
[discord](https://discord.gg/9XpEjMw3Rx).

`Ingredient` type algorithm/function suggestions can go in the ingredients channel.
You can post your creations in the demo channel as well.

# usage

<a name="cli"></a>
## cli

All of the cli commands look like this.

```bash
pyrogis {order} {path} [-o output] [--frames] [...recipe options]
```

`order` is one of
- [chef](#chef)   
- [sort](#sort)   
- [quantize](#quantize)   
- [threshold](#threshold)   

The options `output` and `path` are used for each `recipe` (`sort`, `quantize`, etc.).
A directory can be used for `path`, in which case the program will try to cook each file in the directory.
If an `output` is provided, it should match the expected output.

In addition, each `order` or "menu item" has its own set of options.

|arg|description|default|valid|
|:----:|-----------|:-----:|:---:|
|`recipe`|menu item to cook|`required`|`sort`, `quantize`, `chef`, `threshold`|
|`path`|path to input media|`required`|`dir`, `file`|
|`-o`,`--output`|name of the output directory|`required`|`str`|
|`--frames`|if provided, only frames will be generated|False|flag|

### sort

*sort pixels along an axis*

```bash
pyrogis sort ./input.jpg -o ./output -l 50 -u 180 -t 1
```

![sorted gnome](https://raw.githubusercontent.com/pierogis/pierogis/master/demo/out/gnome_sort.png)

|arg|description|default|valid|
|------|-----------|:-----:|:---:|
|`-l`, `--lower-threshold`|pixels with intensity *below* this value serve as sort boundaries|`64`|`0-255`|
|`-u`, `--upper-threshold`|pixels with intensity *above* this value serve as sort boundaries|`180`|`0-255`|
|`-t`, `--turns`|number of clockwise turns from sorting bottom to top|`0`|`0-3`|
|`--ccw`|if provided, `turns` will be applied counter-clockwise|False|flag|

### quantize

*quantize an image to a smaller set of colors*

![quantized gnome](https://raw.githubusercontent.com/pierogis/pierogis/master/demo/out/gnome_magic.png)

```bash
pyrogis quantize input.jpg -n 16 -r 3 -i 3
```

|arg|description|default|valid|
|:----:|-----------|:-----:|:---:|
|`-n`, `--palette_size`|number of colors in the palette to cluster for|8|`int`|
|`-r`, `--repeats`|number of times to repeat a temperature for DA|1|`int`|
|`-i`, `--iterations`|number of times to repeat an iteration of a coarseness level|1|`int`|
|`--initial_temp`|initial temp to use in DA for optimization|1|`float`|
|`--final_temp`|final temp to use in DA for optimization|0.001|`float`|
|`-d`, `--dithering_level`|relative dithering level (use .5-1.5)|0.8|`float`|

(See more documentation on [`rscolorq`](https://github.com/okaneco/rscolorq))

### chef

*parse text for a recipe*

![sorted and quantized gnome](https://raw.githubusercontent.com/pierogis/pierogis/master/demo/out/gnome_sort_quantize.png)

.txt files and quoted strings can describe a series of CLI recipes, piped from one to the next.

```bash
pyrogis chef ./input.jpg "sort -u 100; quantize" -o ./output
# or
pyrogis chef ./input.jpg recipe.txt -o ./output
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

![threshold gnome](https://raw.githubusercontent.com/pierogis/pierogis/master/demo/out/gnome_threshold.png)

Pixels with brightness outside of the thresholds provided become "included".
Pixels within the thresholds become "excluded".
By default, included means replaced with white, excluded with black.

```bash
pyrogis threshold ./input.jpg -u 150 -l 20 
```
|arg|description|default|valid|
|:----:|-----------|:-----:|:---:|
|-u,--upper-threshold|pixels above this value are white|180|`int`|
|-l,--lower-threshold|pixels below this value are white|64|`int`|
|--include|hex color to substitute for white|ffffff|`str`|
|--exclue|hex color to substitute for black|000000|`str`|

<a name="package"></a>
## package

>*"`pierogis` is the name of the framework;*
>
>*`pyrogis` is the name of the python package and cli tool"*
>
>\- a wise man
```python
import pyrogis
```

[Docs](docs/pyrogis.html) are automatically generated by [pdoc](https://pdoc.dev)

The created files can be found in this repository in the `docs` folder

<a name="acknowledgements"></a>
## acknowledgements

The original python [pixelsort](https://github.com/satyarth/pixelsort) package inspired this package. While the
underlying [algorithm](https://github.com/kimasendorf/ASDFPixelSort) of that package and of `sort` in this one is
supposed to be functionally the same, details of the implementation may differ, and it makes up just part of this package.

The quantizing algorithm used in this package is implemented by [`rscolorq`](https://github.com/okaneco/rscolorq), which
is a port of [`scolorq`](http://people.eecs.berkeley.edu/~dcoetzee/downloads/scolorq/), itself an implementation
of Spatial Color Quantization.
