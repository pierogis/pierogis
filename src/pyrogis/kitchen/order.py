import os
from multiprocessing import Queue
from pathlib import Path
from typing import List, Union, Tuple

import imageio

from .ticket import Ticket


class Order:
    order_name: str
    tickets: List[Ticket]
    failures: "Queue[Tuple[Exception, Ticket]]"
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
    def ticket_output_paths(self):
        for ticket in self.tickets:
            yield ticket.output_path

    @property
    def frames(self) -> int:
        return len(self.tickets)

    @property
    def output_path(self) -> str:
        order_name = self.order_name

        if self._output_path is None:
            if order_name is None:
                order_name = os.path.splitext(os.path.basename(self.input_path))[0]
            if self.frames == 1:
                output_path = order_name + '.png'
            elif self.frames == 0:
                return None
            else:
                output_path = order_name + '.gif'

            self._output_path = output_path

        if self._output_path is not None:
            self._output_path = os.path.expanduser(
                os.path.abspath(self._output_path)
            )

        return self._output_path

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
        self.failures = Queue()
        self._output_path = output_path
        self.fps = fps
        self.duration = duration
        self.optimize = optimize
        self.presave = presave
        self.cook_async = cook_async

        if processes is None:
            processes = os.cpu_count()
        self.processes = processes
        self.resume = resume

    def add_ticket(self, ticket: Ticket):
        self.tickets.append(ticket)
