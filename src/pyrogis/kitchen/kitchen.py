import multiprocessing  as mp
import time
from collections import Callable
from typing import Tuple

from .menu import menu
from .ticket import Ticket


class Kitchen:
    menu = menu

    def __init__(self, chef, report_times: Callable[Tuple[float, float, float]] = None):
        self.chef = chef
        self.pool = mp.Pool()

    @staticmethod
    def cook_ticket(
            chef, output_filename: str,
            ticket: Ticket
    ) -> Tuple[float, float, float]:
        """
        cook a ticket with a thread pool
        """
        assemble_start = time.perf_counter()
        dish = chef.assemble_ticket(ticket, menu)
        assemble_time = time.perf_counter() - assemble_start

        cook_start = time.perf_counter()
        cooked_dish = chef.cook_dish(dish)
        cook_time = time.perf_counter() - cook_start

        save_start = time.perf_counter()
        cooked_dish.save(output_filename)
        save_time = time.perf_counter() - save_start

        return assemble_time, cook_time, save_time

    def queue_ticket(self, output_filename: str, ticket: Ticket, report_times: Callable):
        self.pool.apply_async(
            func=self.cook_ticket,
            args=(self.chef, output_filename, ticket),
            callback=report_times
        )

    def close(self):
        self.pool.close()

    def __getstate__(self):
        self_dict = self.__dict__.copy()
        del self_dict['pool']
        return self_dict

    def __setstate__(self, state):
        self.__dict__.update(state)
