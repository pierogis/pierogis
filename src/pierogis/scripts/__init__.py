import click


@click.group()
def cli():
    pass


from .sort import sort

cli.add_command(sort)
