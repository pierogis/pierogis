import math
import os
import threading
from typing import List, Callable

import imageio as imageio
import numpy as np
from PIL import UnidentifiedImageError
from natsort import natsorted

from .ingredient import Ingredient
from .pierogi import Pierogi
from .recipe import Recipe


class Dish(Ingredient):
    """
    crop and cook an entire recipe for all pixels

    create a Dish from:
    - single Pierogi
    - list of Pierogis
    - image file
    - video file
    - directory
    """

    _pierogis: List[Pierogi] = None
    _frames: int = None
    _fps: int = None

    @property
    def frames(self):
        return len(self.pierogis)

    def prep(
            self,
            pierogis: List[Pierogi] = None,
            recipe:Callable=None,
            fps: float = None,
            **kwargs
    ):
        """
        set the recipe to cook for this dish

        :param recipe: something callable that returns a
        cook(pixels) method.
        Any Ingredient (including recipe) is an example of this

        :param pierogis: a list of Pierogi to cook
        """
        self.pierogis = pierogis
        self.fps = fps

        if recipe is None:
            recipe = Recipe()
        self.recipe = recipe

    def cook(self, pixels: np.ndarray, frame: int = 0) -> np.ndarray:
        return self.recipe(0, 0).cook(self.pierogis[i].pixels)

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
            self,
            path: str,
            optimize: bool = True,
            duration: float = None,
            fps: float = None
    ) -> None:
        """
        :param duration: ms duration between frames
        """
        if len(self.pierogis) > 1:
            ims = [np.asarray(pierogi.image) for pierogi in self.pierogis]
            if duration is not None:
                fps = 1000 / duration

            if fps is None:
                fps = 30

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
