import os
from pathlib import Path
from typing import List, Union

import imageio

from .ticket import Ticket


class Order:
    order_name: str
    tickets: List[Ticket]
    output_path: str
    fps: float
    resume: bool = False
    presave: bool = None
    cook_async: bool = None
    processes: int = None
    _reader = None

    @property
    def order_name(self):
        if self._order_name is None:
            # set order name to first word of input filename if none given
            if os.path.isfile(self.input_path):
                self._order_name = os.path.splitext(
                    os.path.basename(self.input_path)
                )[0].split()[0]

        return self._order_name

    @property
    def reader(self):
        if self._reader is None:
            if os.path.isfile(self.input_path):
                self._reader = imageio.get_reader(self.input_path)

        return self._reader

    @property
    def output_paths(self):
        for ticket in self.tickets:
            yield ticket.output_path

    def __init__(
            self,
            order_name: str,
            input_path: str,
            output_path: Union[str, Path] = None,
            fps: float = None,
            duration: int = None,
            optimize: bool = None,
            presave: bool = None,
            cook_async: bool = None,
            processes: int = None,
            resume: bool = None,
    ):
        self._order_name = order_name
        self.input_path = input_path
        self.tickets = []
        self.output_path = output_path
        self.fps = fps
        self.duration = duration
        self.optimize = optimize
        self.presave = presave
        self.cook_async = cook_async
        self.processes = processes
        self.resume = resume

        if not os.path.isfile(input_path):
            self.presave = False

    def add_ticket(self, ticket: Ticket):
        self.tickets.append(ticket)
