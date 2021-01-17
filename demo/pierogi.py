from pyrogis import *
import numpy as np

if __name__ == '__main__':
    # pixels = np.random.randint(0, 255, (1, 2, 3))
    # ingredient = Ingredient(pixels=pixels)
    # ingredient.show()
    pierogi = Pierogi(path='/Users/kyle/Desktop/c50ef630aded13b32d4acc342ea04857.jpg')

    palette = [
        [100, 210, 69],
        [45, 23, 180],
        [62, 31, 70],
        [10, 210, 240],
        [45, 10, 244],
        [38, 31, 10],
        [255, 255, 255],
        [99, 94, 124]
    ]
    quantize = Quantize(palette=palette)

    # quantize.season(palette=palette)

    # pass in lists to be mixed
    quantize_recipe = Recipe(ingredients=[pierogi, quantize])

    quantize_dish = Dish(recipe=quantize_recipe)

    quantize_dish.serve()
    quantize_dish.show()
