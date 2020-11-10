from PIL import Image

from . import Pierogi
from . import Threshold
from .recipe import Recipe
from . import Mix
from .dish import Dish

image = Image.open('/Users/kyle/Desktop/input1.png')
pierogi = Pierogi(image)

threshold = Threshold(lower_threshold=100, upper_threshold=120)

# pass in lists to be mixed
mix = Mix([pierogi, threshold])
# recipe = Recipe(mix)

dish = Dish(mix, size=pierogi.size)

for dish in dish.serve():

    pass



bites = dish.to_bytes()

cooked_image = Image.frombytes("RGBA", image.size, bites)

cooked_image.show()
pierogi.show()
