from dataclasses import dataclass
from collections.abc import Sequence


@dataclass
class Pixel(Sequence):
    """Just a named list with some helper functions
    """
    r: int = 0
    g: int = 0
    b: int = 0
    # a: int = 0

    # x: int = None
    # y: int = None

    # @property
    # def rgba(self):
    #     return self.r, self.g, self.b, self.a

    @property
    def intensity(self):
        return sum(self) / 3

    # @property
    # def location(self):
    #     return (self.x, self.y)

    # def mix(self, r, g, b, a, opacity: int=80):
    #     self.r = round((self.r * (100 - opacity) / 100) + (r * opacity / 100))
    #     self.g = round((self.g * (100 - opacity) / 100) + (g * opacity / 100))
    #     self.b = round((self.b * (100 - opacity) / 100) + (b * opacity / 100))
    #     self.a = round((self.a * (100 - opacity) / 100) + (a * opacity / 100))

    def __getitem__(self, i):
        if i == 0:
            return self.r
        elif i == 1:
            return self.g
        elif i == 2:
            return self.b
        else:
            raise IndexError

    def __len__(self):
        return 3

    @classmethod
    def mix(cls, under_pixel: 'Pixel', over_pixel: 'Pixel', opacity: int = 100) -> 'Pixel':
        cooked_rgba = []

        for i in range(len(under_pixel)):
            cooked_val = cls.mix_channel(under_pixel[i], over_pixel[i], opacity)

            cooked_rgba.append(cooked_val)

        return cls(*cooked_rgba)

    @staticmethod
    def mix_channel(under_val, over_val, opacity=100):
        return round((under_val * (100 - opacity) / 100) + (over_val * opacity / 100))

    # def place(self, x, y):
    #     return Pixel(*self.rgba, x, y)
