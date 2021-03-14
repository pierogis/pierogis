from typing import List

from .ticket import Ticket


class Order:
    order_name: str
    tickets: List[Ticket]
    fps: float

    def __init__(self, order_name: str):
        self.order_name = order_name
        self.tickets = []

    def add_ticket(self, ticket: Ticket):
        self.tickets.append(ticket)
