import sys

from .kitchen import Chef, Server, Kitchen


def main(args=None):
    """cli program"""
    if args is None:
        args = sys.argv[1:]

    server = Server()

    kitchen = Kitchen(Chef())

    server.take_order(args, kitchen)

    for order in server.orders:
        server.check_order(order, args)


if __name__ == "__main__":
    sys.exit(main())
