from .ingredient import Ingredient

from .pixel import Pixel

class Threshold(Ingredient):
    def __init__(self, upper_threshold=.2, lower_threshold=.8, opacity=100, mix_pixel:Pixel=Pixel()):
        super().__init__(opacity)
        self.upper_threshold = upper_threshold
        self.lower_threshold = lower_threshold
        self.mix_pixel = mix_pixel

    def mix(self, pixel: Pixel):
        if pixel.intensity > self.upper_threshold:
            self.mix_pixel = Pixel(255, 255, 255, 255)
            
        else:
            self.mix_pixel = Pixel(0, 0, 0, 255)

        super().mix(pixel)

        return pixel