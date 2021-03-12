import multiprocessing  as mp

from .menu import menu
from .ticket import Ticket


class Kitchen:
    menu = menu

    def __init__(self, chef):
        self.chef = chef
        mp.set_start_method('spawn')
        self.pool = mp.Pool()

    def cook_ticket(self, output_filename: str, ticket: Ticket):
        """
        cook a ticket with a thread pool
        """
        dish = self.chef.assemble_ticket(ticket, menu)

        cooked_dish = self.chef.cook_dish(dish)

        cooked_dish.save(output_filename)

    def queue_ticket(self, output_filename: str, ticket: Ticket):
        self.pool.apply_async(func=self.cook_ticket, args=(output_filename, ticket))

    def close(self):
        self.pool.close()

    def __getstate__(self):
        self_dict = self.__dict__.copy()
        del self_dict['pool']
        return self_dict

    def __setstate__(self, state):
        self.__dict__.update(state)
