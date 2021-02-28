import os
import sys
import time

from pyrogis import Dish
from .kitchen import Chef, Server, Kitchen, menu


def main(args=None, order_name = None, output_filename=None):
    """cli program"""
    if args is None:
        args = sys.argv[1:]

    server = Server()
    if order_name is None:
        order_name = 'sort'
    tickets = server.take_orders(order_name, args, menu)

    if len(tickets) > 0:
        kitchen = Kitchen([Chef()])
        kitchen.cook_tickets(order_name, tickets)

        # waits for the dishes to all be cooked
        order_dir = os.path.join(server.cooked_dir, str(order_name))
        cooked_tickets = server.check(order_dir)
        while cooked_tickets < len(tickets):
            cooked_tickets = server.check(order_dir)

            time.sleep(1)

        if output_filename is None:
            output_filename = 'sort.png'

        # all cooked
        frame_duration = 15
        fps = None
        optimize = True
        if frame_duration is not None:
            fps = 1000 / frame_duration

        dish = Dish.from_path(order_dir)

        server.togo(order_name, dish, output_filename, fps, optimize)


if __name__ == "__main__":
    sys.exit(main())
