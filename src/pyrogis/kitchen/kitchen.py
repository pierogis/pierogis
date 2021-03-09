# from pierogis_rs import Kitchen
import asyncio
from concurrent.futures.thread import ThreadPoolExecutor

from .ticket import Ticket
from .menu import menu


class Kitchen:
    menu = menu

    def __init__(self, chef):
        self.chef = chef

    async def cook_ticket(self, order_name: str, filename: str, ticket: Ticket):
        """
        cook a ticket with a thread pool
        """
        dish = self.chef.assemble_ticket(ticket, menu)
        await self.chef.cook_dish(order_name, filename, dish)
