# pierogis

[![version](https://img.shields.io/pypi/v/pierogis.svg)](https://pypi.org/project/pierogis/)
[![docs](https://img.shields.io/readthedocs/pierogis/stable.svg)](https://docs.pierogis.live)

[![discord](https://img.shields.io/badge/discord-flat.svg?logo=discord&logoColor=ffffff&color=7389D8)](https://discord.gg/9XpEjMw3Rx)
[![twitter](https://img.shields.io/badge/twitter-flat.svg?logo=twitter&logoColor=ffffff&color=1DA1F2)](https://twitter.com/pierogis_chef)

`pierogis` is a framework for image and animation processing. Ingredients that describe image processing functions can be assembled
into recipes and used to cook an image or animation.

```bash
pip install pierogis
pierogis custom teton.png "resize --width 768 --height 768; sort; quantize; resize --scale 4" -o output.png
# or
pierogis custom teton.png recipe.txt -o output.png
```

`recipe.txt`
```text
resize --width 768 --height 768;
sort;
quantize -c 000000 ffffff 668a61 cbb8a2 b6d655 434d1f 5fb7d2 6d8ab9 3876c1 515b5e a8725f d7b6aa 3c2329 f78693 637186 00407A;
resize -s 4;
```
<p align="center">
  <img align="center" alt="sorted and quantized teton" src="https://media.githubusercontent.com/media/pierogis/pierogis/develop/demo/out/teton.png">
</p>

- [install](#install)
- [features](#features)
- [acknowledgements](#acknowledgements)
- [issues and contributing](#issues-and-contributing)

<a name="install"></a>
## install

**install from a wheel with pip**

```sh
pip install pierogis
```

Depends on `numpy` and `PIL`. PIL requires some external C libraries for handling image files. You probably don't have
to worry about this. If you do, try a `conda` installation.

To build from source (either the repository or the sdist), you will need to install the rust stable toolchain.

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
pip install -r requirements.txt

pip install .
```

Note that the python package was previously called `pyrogis`.
That was supposed to denote the difference between the package
and the Rust algorithms (`pierogis_rs`) that it relied on.

These two parts were combined into one namespace in the `0.4.0` release,
and the split naming became redundant.

Still, `pip install pyrogis==0.4.0` will install `pierogis`.

<a name="features"></a>
## features

- **CLI** - Use a `rich` cli to cook à la carte recipes, or provide a recipe in a document (see [docs](https://docs.pierogis.live/en/stable/cli.html))
- **Animations** - Animations (gifs and movies) can be cooked in one command
- **Extendable** - Easy to create custom manipulations (see [docs](https://docs.pierogis.live/en/stable/ingredients.html#extending))
- **Lazy Rendering** - Render a manipulation after constructing your pipeline (see [docs](https://docs.pierogis.live/en/stable/ingredients.html#dish))
- **Numpy or Rust backend** - Image processing functions use Numpy for (python relative) fast operations. Some
  ingredients use compiled `Rust` for more speed.
  
<p align="center">
  <img align="center" alt="terminal screen" src="https://media.githubusercontent.com/media/pierogis/pierogis/develop/demo/terminal.png">
</p>

<p align="center">
  <img align="center" alt="wires recipe" src="https://media.githubusercontent.com/media/pierogis/pierogis/develop/demo/recipe.png">
</p>

<p align="center">
  <img align="center" src="https://media.githubusercontent.com/media/pierogis/pierogis/develop/demo/out/wires.gif">
</p>

<a name="acknowledgements"></a>
## acknowledgements

The original python [pixelsort](https://github.com/satyarth/pixelsort) package inspired this package. While the
underlying [algorithm](https://github.com/kimasendorf/ASDFPixelSort) of that package and of `sort` in this one is
supposed to be functionally the same, details of the implementation may differ.

A quantization algorithm used in this package uses [`rscolorq`](https://github.com/okaneco/rscolorq), which
is a Rust port of [`scolorq`](http://people.eecs.berkeley.edu/~dcoetzee/downloads/scolorq/),
itself an implementation of Spatial Color Quantization.

An algorithm called
[`MMPX`](https://casual-effects.com/research/McGuire2021PixelArt/index.html)
is used in this package to do 2x image magnification.
It is implemented in a separate [Rust package](https://github.com/pierogis/mmpx-rs).

<a name="issues-and-contributing"></a>
## issues and contributing

When you encounter an error, there are some guidelines that will make it easier to help you:

- Ensure that you are using the latest version of the package. It's early days so errors and updates will be frequent.
  Use `pip uninstall pierogis` then `pip install pierogis --no-cache-dir` to reinstall.
- Provide the version of `pierogis` that you are using in issues to rule that out.
  `pip list` -> pierogis \_.\_.\_
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
