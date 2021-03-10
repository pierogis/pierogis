import sys
import time

from .kitchen import Chef, Server, Kitchen


def main(args=None, order_name=None):
    """cli program"""
    if args is None:
        args = sys.argv[1:]

    server = Server()
    if order_name is None:
        order_name = 'sort'

    kitchen = Kitchen(Chef())
    server.take_orders(order_name, args, kitchen)

    while not server.check_cooked(order_name):
        time.sleep(1)


    # server.togo(dish, order_name)


if __name__ == "__main__":
    sys.exit(main())
