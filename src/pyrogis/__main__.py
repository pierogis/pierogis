import multiprocessing as mp
import sys

from .kitchen import Chef, Server, Kitchen
from .interface import Interface


def main(args=None):
    """cli program"""
    if args is None:
        args = sys.argv[1:]

    server = Server()

    mp.set_start_method('spawn', force=True)
    kitchen = Kitchen(Chef())

    server.take_order(
        args,
        kitchen
    )


if __name__ == "__main__":
    interface = Interface()
    sys.exit(interface.run(main))
