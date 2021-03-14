from typing import List

from .ticket import Ticket


class Order:
    order_name: str
    tickets: List[Ticket]
    fps: float

    def __init__(
            self,
            order_name: str = None,
            output_filename: str = None,
            fps: float = None,
            duration: int = None,
            optimize: bool = None
    ):
        self.order_name = order_name
        self.tickets = []
        self.output_filename = output_filename
        self.fps = fps
        self.duration = fps
        self.optimize = optimize
        self.cook_rate = 0
        self.cook_rate_trend = 0

    def add_ticket(self, ticket: Ticket):
        self.tickets.append(ticket)

    def smooth_cook_rate(self, sample: float):
        alpha = .2
        gamma = 0
        previous_cook_rate = self.cook_rate
        self.cook_rate = alpha * sample + (1 - alpha) * (previous_cook_rate + self.cook_rate_trend)
        cook_rate_change = self.cook_rate - previous_cook_rate

        previous_cook_rate_trend = self.cook_rate_trend
        self.cook_rate_trend = gamma * cook_rate_change + (1 - gamma) * previous_cook_rate_trend
