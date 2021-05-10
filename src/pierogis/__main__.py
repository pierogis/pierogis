import multiprocessing as mp
import sys
from typing import Callable

from .kitchen import LineCook, Server, Kitchen
from .restaurant import Restaurant


def run(args=None, report_callback: Callable = None):
    if args is None:
        args = sys.argv[1:]

    server = Server(report_callback)

    kitchen = Kitchen(LineCook())

    server.take_order(
        args,
        kitchen
    )


def main():
    """cli program"""

    restaurant = Restaurant()
    sys.exit(restaurant.open(run))


if __name__ == '__main__':
    main()
