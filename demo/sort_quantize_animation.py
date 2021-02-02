from pyrogis import *
import numpy as np


def create_sort_quantize_frame(pierogi, upper_threshold, palette_size=16):
    quantize = SpatialQuantize(palette_size=palette_size, iterations=3, repeats=3)
    threshold = Threshold(lower_threshold=0, upper_threshold=upper_threshold)
    sort = Sort(seasoning=threshold)
    quantize_recipe = Recipe(ingredients=[pierogi, sort, quantize])

    quantize_dish = Dish(recipe=quantize_recipe)

    cooked = quantize_dish.serve()

    return cooked.image


if __name__ == '__main__':
    pierogi = Pierogi(file='demo/gnome.jpg')

    image = pierogi.image
    images = []

    for i in range(64):
        print("\rframe {}".format(i))
        cooked_image = create_sort_quantize_frame(pierogi, 4*i, 4)

        images.append(cooked_image)

    a = images[1:]
    a.append(create_sort_quantize_frame(pierogi, 255, 4))

    reversed_images = a[::-1]

    images.extend(reversed_images)

    images[0].save('out.gif', format='GIF', save_all=True, append_images=images[1:], optimize=True, duration=20,
                   loop=0)
