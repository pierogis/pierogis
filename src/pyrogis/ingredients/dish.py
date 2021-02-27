import math
import os
from typing import List

import imageio as imageio
import numpy as np
from PIL import UnidentifiedImageError

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
            self,
            pierogis: List[Pierogi],
            recipe=None,
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

        if recipe is None:
            Recipe()
        self.recipe = recipe

    @classmethod
    def _from_file(cls, file: str) -> 'Dish':
        pierogis = []

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

        return cls(pierogis=pierogis)

    @classmethod
    def from_path(cls, path: str) -> 'Dish':
        pierogis = []

        if os.path.isfile(path):
            return cls._from_file(path)

        files = sorted(os.listdir(path))

        for file in files:
            file_path = os.path.join(path, file)
            if not os.path.isfile(file_path):
                continue
            try:
                pierogis.append(Pierogi(file=file_path))

            except UnidentifiedImageError:
                print("{} is not an image".format(path))

            except ValueError:
                print("{} is not an image".format(path))

            except IsADirectoryError:
                print("{} is a directory".format(path))

        return cls(pierogis=pierogis)

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
            self, path, optimize: bool = True, duration: float = None, fps: float = 25
    ) -> None:
        """
        :param duration: ms duration between frames
        """
        if len(self.pierogis) > 1:
            ims = [np.asarray(pierogi.image) for pierogi in self.pierogis]
            if duration is not None:
                fps = 1000 / duration

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

    def save_frames(
            self,
            frames_dir
    ) -> None:
        """
        :param duration: ms duration between frames
        """
        digits = math.floor(math.log(self.frames, 10)) + 1
        i = 1

        for pierogi in self.pierogis:
            if pierogi.file is None:
                filename = str(i).zfill(digits) + '.png'
            else:
                filename = os.path.basename(pierogi.file)

            frame_filename = os.path.join(frames_dir, filename)

            pierogi.save(frame_filename)

            i += 1
