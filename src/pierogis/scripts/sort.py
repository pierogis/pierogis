import time

import click

from pierogis import *


@click.command()
@click.argument('file')
@click.option('-o', '--output', help='Path and filename to save resulting image')
@click.option('-t', '--turns', default=0,
              help='Clockwise 90 degree turns for the sort direction (0: darker -> lighter, bottom -> top)')
def sort(file, output, turns):
    """
    Sort pixels in an image by intensity
    """

    pierogi = Pierogi(path=file)

    # seasoning is for things that process but don't return a array
    threshold = Threshold(target=pierogi, lower_threshold=64, upper_threshold=180)

    sort = Sort(turns=turns)
    # apply a threshold mask to the sort
    threshold.season(sort)

    sort_recipe = Recipe(ingredients=[pierogi, sort])

    sort_dish = Dish(height=pierogi.height, width=pierogi.width, recipe=sort_recipe)

    sort_dish.serve()

    if output is None:
        file_name = time.strftime("%Y%m%d-%H%M%S")

        output = file_name + ".png"
        click.secho("No output path provided, using " + output, fg='yellow')

    sort_dish.save(output)
