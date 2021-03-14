import multiprocessing as mp
import sys

from rich.align import Align
from rich.console import RenderGroup
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TimeElapsedColumn, TextColumn

from .kitchen import Chef, Server, Kitchen


def main(args=None):
    """cli program"""
    if args is None:
        args = sys.argv[1:]

    server = Server()

    mp.set_start_method('spawn', force=True)
    kitchen = Kitchen(Chef())

    kitchen_progress = Progress(
        TextColumn("[progress.description]{task.description}", justify='right'),
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeElapsedColumn(),
        "[cyan][progress.description]{task.fields[cook_rate]:>5.2f} 🥟 per s",
        refresh_per_second=2
    )

    server_progress = Progress(
        TextColumn("[progress.description]{task.description}", justify='center'),
        refresh_per_second=2
    )

    layout = Layout()

    layout.split(
        Layout(name='kitchen'),
        Layout(name='server'),
        direction="horizontal"
    )

    kitchen_group = RenderGroup(Align("[bold blue]kitchen", style='u', align="center"), kitchen_progress)
    server_group = RenderGroup(Align("[bold blue]server", style='u', align="center"), server_progress)

    layout['kitchen'].update(Panel(kitchen_group))
    layout['kitchen'].ratio = 3
    layout['server'].update(Panel(server_group))

    with Live(layout):
        kitchen_task = kitchen_progress.add_task('...', cook_rate=0)
        server_task = server_progress.add_task('ordering', justify='center')

        def update_cook_task(**kwargs):
            kitchen_progress.update(kitchen_task, refresh = False, **kwargs)

        def update_order_status(**kwargs):
            server_progress.update(server_task, **kwargs)

        server.take_order(
            args,
            kitchen,
            update_cook_task=update_cook_task,
            update_order_status=update_order_status
        )

        for order in server.orders:
            server_progress.update(server_task, description="awaiting")

            server.check_order(
                order,
                update_callback=update_cook_task
            )

            server_progress.update(server_task, description="plating")

            server.togo(order=order)

        server_progress.update(server_task, description="done")


if __name__ == "__main__":
    sys.exit(main())
