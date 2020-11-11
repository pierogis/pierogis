from .ingredient import Ingredient

from .pixel import Pixel


class Threshold(Ingredient):
    def prep(self, **kwargs):
        self.upper_threshold = kwargs.get('upper_threshold', 75)
        self.lower_threshold = kwargs.pop('lower_threshold', 175)

    def cook(self, pixel: Pixel, x: int, y: int):
        if pixel.intensity > self.upper_threshold:
            cooked_pixel = Pixel(255, 255, 255, 255)

        else:
            cooked_pixel = Pixel(0, 0, 0, 255)

        return cooked_pixel
