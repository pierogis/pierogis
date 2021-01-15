import time

from rpierogis import recipes
from pierogis import Threshold
import numpy as np

array = np.random.randint(0, 255, (400, 500, 3))

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
    a = recipes.quantize(array.astype('uint8'), 8)
    pass


if __name__ == '__main__':
    test_quantize()
