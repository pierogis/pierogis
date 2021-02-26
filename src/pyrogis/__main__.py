import sys

from .chef import Chef, Server, Kitchen


def main(args=None):
    """cli program"""
    if args is None:
        args = sys.argv[1:]

    server = Server()
    order_name = 'sort'
    tickets = server.take_orders(order_name, args)

    kitchen = Kitchen([Chef()])
    kitchen.cook_tickets(order_name, tickets)

    # waits for the dishes to all be cooked
    server.plate(order_name)

    output_filename = 'sort.png'
    # all cooked
    while True:
        try:
            server.togo(order_name, output_filename)
            break

        except:
            print("Try again")


if __name__ == "__main__":
    sys.exit(main())
