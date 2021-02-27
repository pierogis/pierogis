# from pierogis_rs import Kitchen
from typing import List

from .chef import Chef


class Kitchen:
    def __init__(self, chefs: List[Chef]):
        self.chefs = chefs

    def cook_tickets(self, tickets, output):
        # waiter takes orders to produce DishDescription
        # chef cooks these dish descriptions (returning Dish)
        # waiter takes these dishes and saves them and plates them

        dishes = []

        for chef in self.chefs:
            # tells chef to start cooking this dish
            # chef saves these somewhere and server remembers?
            chef.cook_tickets(tickets, output)
