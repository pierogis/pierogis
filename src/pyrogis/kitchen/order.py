from typing import List

from .ticket import Ticket


class Order:
    order_name: str
    tickets: List[Ticket]
    fps: float

    def __init__(
            self,
            order_name: str,
            input_path: str,
            output_filename: str = None,
            fps: float = None,
            duration: int = None,
            optimize: bool = None
    ):
        self.order_name = order_name
        self.input_path = input_path
        self.tickets = []
        self.output_filename = output_filename
        self.fps = fps
        self.duration = duration
        self.optimize = optimize

    def add_ticket(self, ticket: Ticket):
        self.tickets.append(ticket)
