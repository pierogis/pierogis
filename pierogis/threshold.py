from .ingredient import Ingredient

from .pixel import Pixel

class Threshold(Ingredient):
    def __init__(self, upper_threshold=.2, lower_threshold=.8, **kwargs):
        super().__init__(**kwargs)
        self.upper_threshold = upper_threshold
        self.lower_threshold = lower_threshold

    def cook(self, pixel: Pixel, x: int, y: int):
        if pixel.intensity > self.upper_threshold:
            cooked_pixel = Pixel(255, 255, 255, 255)
            
        else:
            cooked_pixel = Pixel(0, 0, 0, 255)

        return cooked_pixel