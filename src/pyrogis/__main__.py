import multiprocessing as mp
import sys

from .kitchen import Chef, Server, Kitchen
from .interface import Interface


def main(args=None, report_times=None, report_status=None):
    """cli program"""
    if args is None:
        args = sys.argv[1:]

    server = Server(report_status=report_status)

    mp.set_start_method('spawn', force=True)
    kitchen = Kitchen(Chef(), report_times=report_times)

    server.take_order(
        args,
        kitchen
    )

    for order in server.orders:
        report_status(order, "awaiting")

        server.check_order(
            order
        )

        report_status(order, "plating")

        server.togo(order=order)

        report_status(order, "done")


if __name__ == "__main__":
    interface = Interface()
    sys.exit(interface.run(main))
