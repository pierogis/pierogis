# from pierogis_rs import Kitchen
import asyncio
import concurrent.futures
import multiprocessing as mp
from multiprocessing import Process, Queue

from .ticket import Ticket
from .menu import menu


class Kitchen:
    menu = menu

    def __init__(self, chef):
        self.chef = chef

    def cook_ticket(self, order_name: str, prefix: str, ticket: Ticket):
        """
        cook a ticket with a thread pool
        """
        dish = self.chef.assemble_ticket(ticket, menu)
        self.chef.cook_dish(order_name, prefix, dish)

    # def queue_ticket(self, order_name: str, prefix: str, ticket: Ticket):
    #     Process(target=self.cook_ticket, args=(order_name, prefix, ticket)).start()

