from dataclasses import dataclass

@dataclass
class Pixel:

    r: int = 0
    g: int = 0
    b: int = 0
    a: int = 0

    x: int = None
    y: int = None
    
    @property
    def tuple(self):
        return (self.r, self.g, self.b, self.a)
    
    @property
    def intensity(self):
        return (self.r + self.g + self.b) / 3

    # def mix(self, r, g, b, a, opacity: int=80):
    #     self.r = round((self.r * (100 - opacity) / 100) + (r * opacity / 100))
    #     self.g = round((self.g * (100 - opacity) / 100) + (g * opacity / 100))
    #     self.b = round((self.b * (100 - opacity) / 100) + (b * opacity / 100))
    #     self.a = round((self.a * (100 - opacity) / 100) + (a * opacity / 100))

    