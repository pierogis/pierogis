# changelog

## v0.1.2

- chef
    - redo handling of input dir and unknown output name

- documentation
    - fix some typos in readme

## v0.1.1

- ingredients
    - fix `Quantize.prep` not catching extra kwargs
  
- documentation
    - update readme to reflect changes in package name and quantize

- deploy
    - combine test pypi and normal pypi publish

## v0.1.0

- ingredients
    - `Quantize` (using `rscolorq` or from palette)
    - `Sort` (Numpy implementation)
    - `Recipe` and `Dish`
    - `quantize`, `sort`, and `chef` CLI recipes
    - `Threshold` (in both Numpy and Rust), and `Seasoning`
    - `Flip` and `Rotate`

- deploy
    - release on PyPi
