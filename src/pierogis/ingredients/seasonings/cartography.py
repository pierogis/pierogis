import enum
from collections import namedtuple

Coordinate = namedtuple('Coordinate', ['x', 'y'])


class Direction(enum.Enum):
    NE = 'ne'
    NW = 'nw'
    SE = 'se'
    SW = 'sw'
    N = 'n'
    E = 'e'
    S = 's'
    W = 'w'
    C = 'c'

    def __str__(self):
        return self.value
