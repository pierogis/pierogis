from .dish import Dish
from .ingredient import Ingredient


# a base/pierogi is an image container (pierogi can load it)
# an ingredient has a cook method that will act on a pixel array
# a dish is a frame maker
# a course is an animation maker
# a recipe applies its ingredients' cook method
# a dish applies a recipe starting with a base's pixels
# what happens when you have a course in a recipe
# what is a course's cook method
# maybe it returns the frame that it is working on

class Course:
    def __init__(self, dishes, duration: int=20, optimize=False):
        pass

    def serve(self):
        pass
        # for pierogi in self.dishes:
        #     dish = Dish(pierogi, recipe)
        #
        #     dish.serve()

# different generators at different frames