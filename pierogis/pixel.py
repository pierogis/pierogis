from dataclasses import dataclass

@dataclass
class Pixel:

    r: int = 0
    g: int = 0
    b: int = 0
    a: int = 0

    # x: int = None
    # y: int = None
    
    @property
    def rgba(self):
        return (self.r, self.g, self.b, self.a)
    
    @property
    def intensity(self):
        return (self.r + self.g + self.b) / 3

    # @property
    # def location(self):
    #     return (self.x, self.y)

    # def mix(self, r, g, b, a, opacity: int=80):
    #     self.r = round((self.r * (100 - opacity) / 100) + (r * opacity / 100))
    #     self.g = round((self.g * (100 - opacity) / 100) + (g * opacity / 100))
    #     self.b = round((self.b * (100 - opacity) / 100) + (b * opacity / 100))
    #     self.a = round((self.a * (100 - opacity) / 100) + (a * opacity / 100))

    @classmethod
    def mix(cls, under_pixel, over_pixel, opacity=100):
        under_rgba = under_pixel.rgba
        over_rgba = over_pixel.rgba

        cooked_rgba = []

        for i in range(4):
            cooked_val = cls.mix_channel(under_rgba[i], over_rgba[i], opacity)

            cooked_rgba.append(cooked_val)

        Pixel(*cooked_rgba, *under_pixel.location)

    @staticmethod
    def mix_channel(under_val, over_val, opacity=100):
        return round((under_val * (100 - opacity) / 100) + (over_val * opacity / 100))

    # def place(self, x, y):
    #     return Pixel(*self.rgba, x, y)