from PIL import Image

from . import Pierogi

image = Image.open('/Users/kyle/Desktop/input1.png')
pierogi = Pierogi(image)

i = 0

for pierogi in pierogi.cook():
    
    pass

bites = pierogi.to_bytes()

cooked_pierogi = Image.frombytes("RGBA", image.size, bites)

cooked_pierogi.show()
pierogi.show()