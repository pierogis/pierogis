import sys
import time

from .kitchen import Chef, Server, Kitchen


def main(args=None):
    """cli program"""
    if args is None:
        args = sys.argv[1:]

    server = Server()

    kitchen = Kitchen(Chef())

    order_name = input("What is the name for this order?")

    server.take_order(args, kitchen, order_name)

    while len(server.order_tickets) > 0:
        for order_name in server.order_tickets.keys():
            if server.check_order(order_name):
                server.order_tickets.pop(order_name)
                server.togo(order_name)

        time.sleep(1)


if __name__ == "__main__":
    sys.exit(main())
