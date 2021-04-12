# pierogis

`pierogis` is a framework for image and animation processing. Ingredients that describe image processing functions can be assembled
into recipes and used to cook an image or animation.

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
pip install -r requirements.txt

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

[Docs](https://docs.pierogis.live/) for cli and package use.
  
![terminal program](https://raw.githubusercontent.com/pierogis/pierogis/develop/demo/terminal.png)

![wires recipe](https://raw.githubusercontent.com/pierogis/pierogis/develop/demo/recipe.png)

![wires gif](https://raw.githubusercontent.com/pierogis/pierogis/develop/demo/out/wires.gif)

<a name="acknowledgements"></a>
## acknowledgements

The original python [pixelsort](https://github.com/satyarth/pixelsort) package inspired this package. While the
underlying [algorithm](https://github.com/kimasendorf/ASDFPixelSort) of that package and of `sort` in this one is
supposed to be functionally the same, details of the implementation may differ.

A quantization algorithm used in this package uses [`rscolorq`](https://github.com/okaneco/rscolorq), which
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

<a name="disclaimer"></a>
## disclaimer

This library is licensed under the [AGPL v3](LICENSE).

Art used for demos is the property of their respective owners.

The following statements are not necessarily legally binding.
If they seem to contradict the license, follow the license.

The licenses of packages used by this software vary, but are understood to be compatible with AGPL.
If you take issue with this package's use of other software regardless of legal concern,
please reach out, and it can be removed from this package.

Also understand that there may be implications from *those* licenses on your use of *this* package.

Review the AGPL yourself if you intend to use this package in any software,
but know that it was chosen to encourage that all related works be open source.

The use of AGPL does not mean that this cannot be monetized,
but it does generally mean that you will need to share source code of improvements on this package;
at least modules related to this package.

If your paid derivative work adds marginal value to what is included in this package,
the author reserves the right to go to great lengths to make a free (and better) alternative to your derivative work.

Please think twice about minting NFTs for works made with this package, especially if they are ugly.
Consider that you do
[communal damage](https://memoakten.medium.com/the-unreasonable-ecological-cost-of-cryptoart-2221d3eb2053)
by trying to profit individually.
