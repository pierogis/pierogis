from typing import Callable

from rich.align import Align
from rich.columns import Columns
from rich.console import RenderGroup
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TimeElapsedColumn, TextColumn


class Interface:
    def __init__(self):
        self.order_tasks = {}
        self.kitchen_progress = Progress(
            TextColumn("[progress.description]{task.description}", justify='right'),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeElapsedColumn(),
            "[cyan][progress.description]{task.fields[cook_rate]:>5.2f} 🥟 per s",
            refresh_per_second=2
        )

        self.server_progress = Progress(
            TextColumn("[progress.description]{task.description}", justify="center"),
            expand=True,
            refresh_per_second=2
        )

    def add_kitchen_task(self, order):
        self.order_tasks[order]['kitchen'] = self.kitchen_progress.add_task('...', cook_rate=0)

    def add_server_task(self, order):
        self.order_tasks[order]['server'] = self.server_progress.add_task('...')

    def run(self, main: Callable):
        kitchen_group = RenderGroup(Align("[bold blue]kitchen", style='u', align="center"), self.kitchen_progress)
        server_group = RenderGroup(Align("[bold blue]server", style='u', align="center"), self.server_progress)

        panels = Columns([Panel(server_group, width=16), Panel(kitchen_group)], expand=True)
        with Live(panels):
            main(report_times=self.report_times, report_status=self.report_status)

    def report_status(self, order, status):
        server_task = self.order_tasks[order.order_name]
        self.server_progress.update(server_task, description=status)
