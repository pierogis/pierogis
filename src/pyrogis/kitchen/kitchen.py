# from pierogis_rs import Kitchen
from concurrent.futures.thread import ThreadPoolExecutor

from .menu import menu


class Kitchen:
    menu = menu

    def __init__(self, chef_type):
        self.chef_type = chef_type
        self.executor = ThreadPoolExecutor()

    def cook_ticket(self, order_name, cooked_dir, ticket):
        # waiter takes orders to produce DishDescription
        # chef cooks these dish descriptions (returning Dish)
        # waiter takes these dishes and saves them and plates them
        self.executor.submit(self.chef_type.cook_ticket, order_name, cooked_dir, ticket, menu)
