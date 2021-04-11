"""
define objects for running the program with rich terminal feedback
"""

import os
import time
from datetime import timedelta
from typing import Callable, Iterable, List

from rich.align import Align
from rich.console import RenderGroup, Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, Task, ProgressColumn, SpinnerColumn
from rich.rule import Rule
from rich.table import Column
from rich.text import Text
from rich.tree import Tree

from .kitchen.order import Order


class TimeElapsedMsColumn(ProgressColumn):
    """show time elapsed with decimal ms"""

    def __init__(self, decimal_places: int = 1, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.decimal_places = decimal_places

    def render(self, task: Task) -> Text:
        """Show time remaining."""
        elapsed = task.finished_time if task.finished else task.elapsed
        if elapsed is None:
            return Text("-:--:--.---", style="progress.elapsed")
        delta = timedelta(milliseconds=elapsed * 1000)
        split = str(delta).split('.')
        rate_string = "{}.{}".format(split[0], split[1][:self.decimal_places])

        return Text(rate_string, style="progress.elapsed")


class TreeColumn(ProgressColumn):
    """show a tree off of the description with branches"""

    def __init__(self, width: int = 15, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.width = width

    def render(self, task: Task) -> Tree:
        """show tree with order name and input files"""

        tree = Tree(('[bold]' + task.description).center(self.width))

        branches = task.fields.get('branches')

        for path in branches:
            tree.add(os.path.basename(path), style='bold red')

        return tree


class SmoothRateColumn(ProgressColumn):
    """update and display an exponential smoothed rate"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.completed = 0
        self.smooth_rate = 0
        self.alpha = .2
        self.last_time = None

    def render(self, task: Task) -> Text:
        current_time = time.perf_counter()

        if self.last_time is None:
            self.last_time = time.perf_counter()

        elapsed = current_time - self.last_time

        completed = task.completed
        total = task.total

        # only smooth every second
        if elapsed > 1 and completed != total:
            rate_sample = (completed - self.completed) / elapsed
            self.smooth_rate = self.alpha * rate_sample + (1 - self.alpha) * self.smooth_rate

            self.completed = completed
            self.last_time = current_time

        rate_string = "{rate:>6.2f}🥟/s".format(rate=self.smooth_rate)
        return Text(rate_string)


class Restaurant:
    """run the main program injected with callbacks to display a rich terminal"""

    def __init__(self):
        self.kitchen_tasks = {}
        self.server_tasks = {}

        self.console = Console()

        # for displaying the kitchen's status cooking orders
        self.kitchen_progress = Progress(
            TreeColumn(),
            BarColumn(),
            " [progress.percentage]{task.percentage:>3.0f}% ",
            TimeElapsedMsColumn(),
            SmoothRateColumn()
        )

        # for displaying the stage of orders/kitchen
        self.server_progress = Progress(
            TextColumn(
                "[bold][progress.description]{task.description}",
                justify="center", table_column=Column(width=12)
            ),
            TextColumn("|"),
            SpinnerColumn('arc', speed=1, finished_text='[bold]✓'),
            TextColumn("{task.fields[input_path]}"),
            TextColumn("[bold blue]->"),
            TextColumn("{task.fields[output_path]}")
        )

    def add_kitchen_task(self, order_name: str, input_paths: Iterable[str]):
        task = self.kitchen_progress.add_task(description=order_name, branches=input_paths, cook_rate=0)
        self.kitchen_tasks[order_name] = task
        return task

    def add_server_task(self, order_name: str, input_path: str, output_path: str):
        task = self.server_progress.add_task('...', input_path=input_path, output_path=output_path)
        self.server_tasks[order_name] = task
        return task

    def open(self, run: Callable):
        """open the restaurant using a provided callable"""
        kitchen_group = RenderGroup(Rule("[bold blue]kitchen"),
                                    Align(self.kitchen_progress, align='center'))
        server_group = RenderGroup(Rule("[bold blue]server"),
                                   Align(self.server_progress, align='center'))

        aligned_server_panel = Align(Panel(server_group, expand=False), align='center')
        aligned_kitchen_panel = Align(Panel(kitchen_group), align='center')

        panels = RenderGroup(aligned_kitchen_panel, aligned_server_panel)
        with Live(panels, refresh_per_second=10, console=self.console):
            try:
                run(report_callback=self._report)
            except KeyboardInterrupt:
                pass

    @staticmethod
    def _get_order_name(order: Order) -> str:
        if order.order_name is not None:
            order_name = order.order_name
        else:
            # set order name to first word of input filename if none given
            order_name = os.path.splitext(
                os.path.basename(order.input_path)
            )[0].split()[0]

        return order_name

    def _report(
            self, order: Order, status: str = None,
            completed: int = None, advance: int = None,
            total: int = None, branches: List[str] = None
    ):
        self._update_server(order, status)
        self._update_kitchen(order, completed, total, advance, branches)

    def _update_server(
            self,
            order: Order,
            status: str
    ):
        order_name = self._get_order_name(order)
        server_task = self.server_tasks.get(order_name)

        input_path = os.path.basename(order.input_path)

        if order.output_path is None:
            output_path = '...'
        else:
            output_path = os.path.basename(order.output_path)

        if server_task is None:
            server_task = self.add_server_task(order_name, input_path, output_path)
        if status is not None:
            self.server_progress.update(server_task, description=status)
            self.server_progress.update(server_task, input_path=input_path)
            self.server_progress.update(server_task, output_path=output_path)
            if status == 'done':
                self.server_progress.update(server_task, total=0)

    def _update_kitchen(self, order: Order, completed: int, total: int, advance: int, branches: List[str]):
        order_name = self._get_order_name(order)

        kitchen_task = self.kitchen_tasks.get(order_name)
        if kitchen_task is None:
            kitchen_task = self.add_kitchen_task(order_name, [])
        if completed is not None:
            self.kitchen_progress.update(kitchen_task, completed=completed)
        if total is not None:
            self.kitchen_progress.update(kitchen_task, total=total)
        if advance is not None:
            self.kitchen_progress.update(kitchen_task, advance=advance)
        if branches is not None:
            self.kitchen_progress.update(kitchen_task, branches=branches)
