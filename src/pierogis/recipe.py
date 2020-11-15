from .mix import Mix

class Recipe(Mix):
    def __init__(self, steps):
        self.steps = steps

    def add(self, ingredients):
        self.steps.append(ingredients)

    # def cook(self):
    #     """Provide a pixel by pixel iterator of the manipulation
    #     """

    #     for step in self.steps:
    #         mix = step.pop(0)
    #         for ingredient in step:
    #             # should be a generator
    #             for y in range(mix.height):
    #                 for x in range(mix.width):
    #                     under_pixel = mix.pixel_array[x][y]
    #                     mix = ingredient.mix(under_pixel)

    #                     pierogi.pixel_array[x][y] = threshold.mix(pixel)

    #                     yield Pierogi()
