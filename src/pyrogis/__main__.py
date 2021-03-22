import multiprocessing as mp
import sys
from typing import Callable

from .kitchen import Chef, Server, Kitchen, Order
from .restaurant import Restaurant


def main(args=None, report_status: Callable = None):
    """cli program"""
    if args is None:
        args = sys.argv[1:]

    server = Server(report_status)

    mp.set_start_method('spawn', force=True)
    kitchen = Kitchen(Chef())

    server.take_order(
        args,
        kitchen
    )


restaurant = Restaurant()
sys.exit(restaurant.run(main))
