import os
from typing import List

import imageio as imageio
import numpy as np

from .ingredient import Ingredient
from .pierogi import Pierogi
from .recipe import Recipe


class Dish(Ingredient):
    """
    crop and cook an entire recipe for all pixels
    """

    @property
    def frames(self):
        return len(self.pierogis)

    def prep(
            self, recipe=None,
            pierogis: List[Pierogi] = None,
            file=None,
            path=None,
            **kwargs
    ):
        """
        set the recipe to cook for this dish

        :param recipe: something callable that returns a
        cook(pixels) method.
        Any Ingredient (including recipe) is an example of this

        :param pierogis: a list of Pierogi to cook

        :param file: a file to use as input to

        :param path: a list of Pierogi to cook
        """

        if pierogis is None:
            pierogis = []

            if file is not None:
                try:
                    # first try to load as video/animation
                    images = imageio.mimread(file, memtest=False)
                    for image in images:
                        pierogis.append(
                            Pierogi(pixels=np.rot90(
                                np.asarray(image), axes=(1, 0)
                            ))
                        )

                except ValueError:
                    # then load as a single image
                    pierogis = [Pierogi(file=file)]

            elif path is not None:
                pierogis = self.get_path_pierogis(path)

            else:
                raise ValueError("Could not create pierogis")

        self.pierogis = pierogis

        if recipe is None:
            Recipe()
        self.recipe = recipe

    @staticmethod
    def get_path_pierogis(path: str) -> List[Pierogi]:
        pierogis = []

        for file in os.listdir(path):
            if not os.path.isfile(file):
                continue

            pierogis.append(Pierogi(file=file))

        return pierogis

    def cook(self, pixels: np.ndarray) -> np.ndarray:
        return self.recipe(0, 0).cook(self.pierogis[0].pixels)

    def serve(self) -> 'Dish':
        """
        cook the recipe and set the output to this object's pixel array
        """

        cooked_pierogis = []

        for frame in range(self.frames):
            pierogi = self.pierogis[frame]
            # cook with these pixels as first input
            recipe = self.recipe(frame + 1, self.frames)
            cooked_pixels = recipe.cook(pierogi.pixels)
            # ensure that the cooked pixels do not overflow 0-255
            clipped_pixels = np.clip(cooked_pixels, 0, 255)
            # # set the objects own pixels to the result of cooking
            cooked_pierogi = Pierogi(pixels=clipped_pixels)

            cooked_pierogis.append(cooked_pierogi)

        return Dish(pierogis=cooked_pierogis)

    def save(
            self, path, optimize: bool = True, duration: float = None, fps: int = 25
    ) -> None:
        """
        :param duration: s duration between frames
        """
        if len(self.pierogis) > 1:
            ims = [np.asarray(pierogi.image) for pierogi in self.pierogis]
            if duration is not None:
                imageio.mimwrite(
                    path,
                    ims=ims,
                    duration=duration,
                    fps=fps
                )
            else:
                imageio.mimwrite(
                    path,
                    ims=ims,
                    fps=fps
                )

            if optimize and os.path.splitext(path)[1] == ".gif":
                try:
                    import pygifsicle
                    pygifsicle.optimize(path)
                except FileNotFoundError as err:
                    print(err)

        elif len(self.pierogis) == 1:
            self.pierogis[0].save(path)

        else:
            raise Exception("Dish has no pierogis")

    #
    # @property
    # def width(self):
    #     """
    #     width from self.pixels
    #     """
    #     return self.base.shape[0]
    #
    # @property
    # def height(self):
    #     """
    #     height from self.pixels
    #     """
    #     return self.recipe.base.shape[1]
    #
    # @property
    # def shape(self):
    #     """
    #     (width, height, 3)
    #     """
    #     return self.width, self.height, 3
