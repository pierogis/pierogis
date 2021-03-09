# from pierogis_rs import Kitchen
from concurrent.futures.thread import ThreadPoolExecutor

from .ticket import Ticket
from .menu import menu


class Kitchen:
    menu = menu

    def __init__(self, chef):
        self.chef = chef
        self.executor = ThreadPoolExecutor()

    def cook_ticket(self, order_name, cooked_dir, ticket: Ticket):
        # waiter takes orders to produce DishDescription
        # chef cooks these dish descriptions (returning Dish)
        # waiter takes these dishes and saves them and plates them
        dish = self.chef.assemble_ticket(ticket, menu)
        self.executor.submit(self.chef.cook_dish, order_name, cooked_dir, dish)
