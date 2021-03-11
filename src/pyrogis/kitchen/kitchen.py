from multiprocessing import Process
from threading import Thread

from .ticket import Ticket
from .menu import menu


class Kitchen:
    menu = menu

    def __init__(self, chef):
        self.chef = chef

    def cook_ticket(self, output_filename: str, ticket: Ticket):
        """
        cook a ticket with a thread pool
        """
        dish = self.chef.assemble_ticket(ticket, menu)

        cooked_dish = self.chef.cook_dish(dish)

        cooked_dish.save(output_filename)

    def queue_ticket(self, output_filename, ticket):
        self.cook_ticket(output_filename, ticket)
        # Process(target=self.cook_ticket, args=(output_filename, ticket)).start()
