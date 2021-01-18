import time

from PIL import Image
from rpierogis import recipes
from pyrogis import Threshold, Ingredient
import numpy as np

array = np.random.randint(0, 255, (100, 100, 3))

def test_threshold():
    upper_threshold = 100
    include_pixel = np.asarray([255.0, 255, 255])
    exclude_pixel = np.asarray([0.0, 0, 0])

    threshold = Threshold(upper_threshold=upper_threshold, include_pixel=include_pixel, exclude_pixel=exclude_pixel)

    start = time.time()
    rthe = threshold.cook(array)
    print(time.time() - start)

    start = time.time()
    npres = threshold.cook_np(array)
    print(time.time() - start)

    # slice
    start = time.time()
    slice = recipes.threshold(array.astype('uint8'), upper_threshold, include_pixel, exclude_pixel)
    print(time.time() - start)
    # slice is super performant at all size images

    # # ndarray
    # start = time.time()
    # nd = ingredients.threshold(array.astype(dtype=np.dtype(float)), upper_threshold, include_pixel, exclude_pixel)
    # print(time.time() - start)
    # # ndarray is really good with small images, and like 33% better than numpy with large ones

def test_sort():
    recipes.sort(array.astype('uint8'), 100)

def test_quantize():

    array = np.array(Image.open("./demo/gnome_small.jpg").convert('RGB'))
    Ingredient(array).show()
    a = recipes.quantize(
        array.astype(dtype=np.dtype('uint8')),
        palette_size=4,
        iters_per_level=3,
        repeats_per_temp=1,
        initial_temp=1,
        final_temp=.001,
        filter_size=3,
        dithering_level=.8,
        seed=0
    )
    Ingredient(a).show()
    pass


if __name__ == '__main__':
    test_quantize()
