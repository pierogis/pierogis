# pierogis

`pierogis` is a framework for image and animation processing. Ingredients that describe image processing functions can be assembled
into recipes and used to cook an image or animation.

`pyrogis` is a python library and cli tool implementing this framework.

```bash
pip install pyrogis
pyrogis chef input.png "sort; quantize" -o output.png
```

![terminal program](https://raw.githubusercontent.com/pierogis/pierogis/main/demo/out/terminal.png)


[Docs](https://pierogis.github.io/pierogis/pyrogis.html) for cli and package use.

![sorted and quantized gnome](https://raw.githubusercontent.com/pierogis/pierogis/main/demo/out/gnome_sort_quantize.png)

- [install](#install)
- [features](#features)
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

To build from source (either the repository or the sdist), you will need to install the rust stable toolchain.

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

pip install .
```

<a name="features"></a>

## features

- **CLI** - Use a `rich` cli to cook à la carte recipes, or provide a recipe in a document
- **Animations** - Animations (gifs and movies) can be cooked in one command
- **Extendable** - Easy to create custom manipulations (see [package](#package))
- **Lazy Rendering** - Render a manipulation after constructing your pipeline (see [package](#package))
- **Numpy or Rust backend** - Image processing functions use Numpy for (python relative) fast operations. Some
  ingredients use compiled `Rust` for more speed.

<a name="acknowledgements"></a>
## acknowledgements

The original python [pixelsort](https://github.com/satyarth/pixelsort) package inspired this package. While the
underlying [algorithm](https://github.com/kimasendorf/ASDFPixelSort) of that package and of `sort` in this one is
supposed to be functionally the same, details of the implementation may differ.

The quantizing algorithm used in this package is done with [`rscolorq`](https://github.com/okaneco/rscolorq), which
is a port of [`scolorq`](http://people.eecs.berkeley.edu/~dcoetzee/downloads/scolorq/), itself an implementation of
Spatial Color Quantization.

<a name="issues-and-contributing"></a>
## issues and contributing

When you encounter an error, there are some guidelines that will make it easier to help you:

- Ensure that you are using the latest version of the package. It's early days so errors and updates will be frequent.
  Use `pip uninstall pyrogis` then `pip install pyrogis --no-cache-dir` to reinstall.
- Provide the version of `pyrogis` that you are using in issues to rule that out.
  `pip list` -> pyrogis \_.\_.\_
- Provide the traceback or error message if relevant.
- Provide your os and any other specific information about how you are trying to use the package.
- Provide the code or the cli command that triggered the error.
- If the problem is visual: that can be more difficult to debug. Share a link to an image hosting site if you want to
  share what you are seeing in an issue.
- If you are getting different behavior than you expect: that could be an error or a feature.
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
