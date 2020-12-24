import os
import time

import click

from pierogis import *


@click.command()
@click.argument('path')
@click.option('-o', '--output', help='Path and filename to save resulting image')
@click.option('-t', '--turns', default=0,
              help='Clockwise 90 degree turns for the sort direction (0: darker -> lighter, bottom -> top)')
def sort(path, output, turns):
    """
    Sort pixels in an image by intensity
    """

    if os.path.isdir(path):
        files = [path + '/' + filename for filename in os.listdir(path)]

    elif os.path.isfile(path):
        files = [path]

    for file in files:
        try:
            pierogi = Pierogi(path=file)
        except Exception as err:
            print(err)
            continue

        # seasoning is for things that process but don't return a array
        threshold = Threshold(target=pierogi, lower_threshold=64, upper_threshold=180)

        sort = Sort(turns=turns)
        # apply a threshold mask to the sort
        threshold.season(sort)

        sort_recipe = Recipe(ingredients=[pierogi, sort])

        sort_dish = Dish(height=pierogi.height, width=pierogi.width, recipe=sort_recipe)

        sort_dish.serve()

        output_filename = output
        if output_filename is None:
            file_name = time.strftime("%Y%m%d-%H%M%S")

            output_filename = file_name + ".png"
            click.secho("No output path provided, using " + output_filename, fg='yellow')

        sort_dish.save(output_filename)
