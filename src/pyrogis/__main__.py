import sys
import time

from .kitchen import Chef, Server, Kitchen


def main(args=None):
    """cli program"""
    if args is None:
        args = sys.argv[1:]

    server = Server()

    kitchen = Kitchen(Chef())

    server.take_order(args, kitchen)

    kitchen.close()

    for order_name in server.order_names:
        while True:
            if server.check_order(order_name):
                server.togo(args=args, order_name=order_name)
                break
            else:
                time.sleep(1)


if __name__ == "__main__":
    sys.exit(main())
