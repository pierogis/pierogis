import os
import time
from datetime import timedelta
from typing import Callable

from rich.align import Align
from rich.console import RenderGroup, Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, Task, ProgressColumn
from rich.text import Text
from rich.tree import Tree

from .kitchen.order import Order


class TimeElapsedMsColumn(ProgressColumn):
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

    def render(self, task: Task) -> Tree:
        """show tree with order name and input files"""

        tree = Tree('[bold]' + task.description)

        input_paths = task.fields.get('input_paths')

        for path in input_paths:
            tree.add(os.path.basename(path))

        return tree

class SmoothCookRateColumn(ProgressColumn):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.completed = 0
        self.smooth_cook_rate = 0
        self.alpha = .2
        self.last_time = time.perf_counter()

    def render(self, task: Task) -> Text:
        completed = task.completed
        current_time = time.perf_counter()

        elapsed = current_time - self.last_time
        cook_rate_sample = (completed - self.completed) / elapsed
        self.smooth_cook_rate = self.alpha * cook_rate_sample + (1 - self.alpha) * self.smooth_cook_rate

        self.completed = completed
        self.last_time = current_time

        rate_string = "{cook_rate:>6.2f}🥟/s".format(cook_rate=self.smooth_cook_rate)
        return Text(rate_string)


class Restaurant:
    def __init__(self):
        self.kitchen_tasks = {}
        self.server_tasks = {}

        self.console = Console()

        self.kitchen_progress = Progress(
            # TextColumn("[bold][progress.description]{task.description}", justify="center"),
            TreeColumn(),
            BarColumn(bar_width=10),
            " [progress.percentage]{task.percentage:>3.0f}% ",
            TimeElapsedMsColumn(),
            SmoothCookRateColumn(),
            # "[bold cyan][progress.description]{task.fields[cook_rate]:>6.2f}🥟/s",
            console=self.console,
            refresh_per_second=2
        )

        self.server_progress = Progress(
            TextColumn("[bold][progress.description]{task.description}", justify="center"),
            console=self.console,
            refresh_per_second=2
        )

    def add_kitchen_task(self, order_name: str, input_path:str):
        task = self.kitchen_progress.add_task(description=order_name, input_paths=[input_path], cook_rate=0)
        self.kitchen_tasks[order_name] = task
        return task

    def add_server_task(self, order_name: str):
        task = self.server_progress.add_task('...')
        self.server_tasks[order_name] = task
        return task

    def open(self, main: Callable):
        kitchen_group = RenderGroup(Text.from_markup("[bold blue]kitchen", style='u', justify='center'),
                                    Align(self.kitchen_progress, align='right'))
        server_group = RenderGroup(Text.from_markup("[bold blue]server", style='u', justify="center"),
                                   Align(self.server_progress, align='center'))

        aligned_kitchen_panel = Align(Panel(server_group, width=20), align='center')
        aligned_server_panel = Align(Panel(kitchen_group, width=60), align='center')

        panels = RenderGroup(aligned_kitchen_panel, aligned_server_panel)
        with Live(panels, refresh_per_second=10):
            main(report_status=self.report_status)

    def report_status(self, order: Order, status: str = None,
                      completed: int = None, advance: int = None, total: int = None,
                      cook_async: bool = None, presave: bool = None):
        order_name = order.order_name
        input_path = order.input_path

        if order_name is None:
            # set order name to first word of input filename if none given
            order_name = os.path.splitext(
                os.path.basename(input_path)
            )[0].split()[0]

        server_task = self.server_tasks.get(order_name)
        if server_task is None:
            server_task = self.add_server_task(order_name)
        if status is not None:
            self.server_progress.update(server_task, description=status)

        kitchen_task = self.kitchen_tasks.get(order_name)
        if kitchen_task is None:
            kitchen_task = self.add_kitchen_task(order_name, input_path)
        if completed is not None:
            self.kitchen_progress.update(kitchen_task, completed=completed)
        if total is not None:
            self.kitchen_progress.update(kitchen_task, total=total)
        if advance is not None:
            self.kitchen_progress.update(kitchen_task, advance=advance)
        # if cook_rate is not None:
        #     self.kitchen_progress.update(kitchen_task, cook_rate=cook_rate)

        input_path = order.input_path
        if input_path is not None:
            input_paths = self.kitchen_progress.tasks[kitchen_task].fields['input_paths']
            if input_path not in input_paths:
                self.kitchen_progress.update(kitchen_task, input_paths=input_paths.append(input_path))
