# changelog

## v0.1.3

- ingredients
    - threshold default behavior change
  
- chef
    - menu items as separate classes from chef
  
- package
    - lots of formatting/lint fixes, notably subpackage imports
    - documentation improvements

- tests
    - threshold tests added

## v0.1.2

- chef
    - redo handling of input dir and unknown output name
    - add quiet flag

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
