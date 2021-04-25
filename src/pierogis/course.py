import os
import subprocess
from pathlib import Path
from typing import List, Union

import imageio
import imageio_ffmpeg
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
            fps: float = None,
            audio_path: Union[str, Path] = None,
            audio_codec: str = None,
    ) -> None:
        """
        :param path: path to save output
        :param optimize: whether or not to try to optimize a gif output with gifsicle
        :param duration: ms duration between frames (gets converted into fps)
        :param fps: frames per second for image
        :param audio_path: audio input file path
        :param audio_codec: ffmpeg audio codec
        """
        if len(self.dishes) > 1:
            if duration is not None:
                fps = 1000 / duration

            if fps is None:
                if self._fps is None:
                    fps = 30
                else:
                    fps = self._fps

            ext = os.path.splitext(path)[1]

            if ext == ".gif":
                # 30/60 fps is impossible for gif because maximum decimal precision is 2
                # (duration .03 rounds to 25fps)
                writer = imageio.get_writer(
                    path,
                    fps=fps
                )

                for dish in self.dishes:
                    writer.append_data(np.asarray(dish.pierogi.image))

            else:
                if ext == ".webm":
                    if audio_codec is None:
                        audio_codec = 'libvorbis'
                    writer = imageio_ffmpeg.write_frames(
                        path,
                        size=self.dishes[0].pierogi.pixels.shape[:2],
                        fps=fps,
                        codec='libvpx-vp9',
                        bitrate='0',
                        output_params=['-crf', '30'],
                        input_params=['-thread_queue_size', '128'],
                        audio_path=audio_path,
                        audio_codec=audio_codec
                    )
                else:
                    writer = imageio_ffmpeg.write_frames(
                        path,
                        size=self.dishes[0].pierogi.pixels.shape[:2],
                        fps=fps,
                        audio_path=audio_path,
                        audio_codec=audio_codec
                    )

                writer.send(None)

                for dish in self.dishes:
                    writer.send(np.asarray(dish.pierogi.image))

            writer.close()

            if optimize and ext == '.gif':
                try:
                    return_code = subprocess.call(
                        ['gifsicle', '--optimize', path, '--output', path],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                except:
                    return_code = 1

                if return_code != 0:
                    print("install gifsicle and ensure it's on PATH to optimize gif")

        elif len(self.dishes) == 1:
            self.dishes[0].pierogi.save(path, optimize=optimize)

        else:
            raise Exception("Dish has no pierogis")
