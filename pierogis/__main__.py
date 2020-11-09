from PIL import Image

from . import Pierogi
from . import Threshold
from . import Recipe

image = Image.open('/Users/kyle/Desktop/input1.png')
pierogi = Pierogi(image)

threshold = Threshold(lower_threshold=100, upper_threshold=120)

# pass in lists to be mixed
recipe = Recipe().add([pierogi, threshold])

for pierogi in recipe.cook():
    cooked_pierogi = pierogi
    pass

bites = cooked_pierogi.to_bytes()

cooked_image = Image.frombytes("RGBA", image.size, bites)

cooked_image.show()
pierogi.show()
