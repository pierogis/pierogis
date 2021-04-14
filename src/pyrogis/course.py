import os
import subprocess
from typing import List

import imageio
import numpy as np

from .ingredients.dish import Dish


class Course:
    """treat a series of Dishes as a unit (animation)"""

    _frames: int = None
    _fps: int = None

    @property
    def frames(self):
        return len(self.dishes)

    def __init__(
            self,
            dishes: List[Dish] = None,
            fps: float = None,
    ):
        self.dishes = dishes
        self.fps = fps

    def serve(self):
        cooked_dishes = []

        for frame in range(self.frames):
            dish = self.dishes[frame]
            # cook with these pixels as first input
            cooked_dish = dish.serve()

            cooked_dishes.append(cooked_dish)

        return Course(cooked_dishes)

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
        if len(self.dishes) > 1:
            if duration is not None:
                fps = 1000 / duration

            if fps is None:
                if self._fps is None:
                    fps = 30
                else:
                    fps = self._fps

            writer = imageio.get_writer(
                path,
                fps=fps
            )

            for dish in self.dishes:
                writer.append_data(np.asarray(dish.pierogi.image))

            writer.close()

            if optimize and os.path.splitext(path)[1] == ".gif":
                try:
                    return_code = subprocess.call(
                        ["gifsicle", '--optimize', path, "--output", path],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                except:
                    return_code = 1

                if return_code != 0:
                    print("install gifsicle and ensure it's on PATH to optimize gif")

        elif len(self.dishes) == 1:
            self.dishes[0].pierogi.save(path)

        else:
            raise Exception("Dish has no pierogis")
