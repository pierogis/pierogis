"""
define an image wrapper ingredient
"""
from typing import Callable

import imageio
import numpy as np
from PIL import Image

from .ingredient import Ingredient


class Pierogi(Ingredient):
    """
    image container for iterative pixel manipulation

    create a Pierogi from:
    - pixel array
    - video file with a frame index
    - image file
    - PIL image
    -

    unless pixels are provided explicitly ( Pierogi(pixels=pixels) ),
    the pixels member is a property that is lazy loaded
    (usually from a file) and cached
    """

    RESAMPLE = Image.NEAREST
    """default resize algorithm is nearest neighbor"""

    _pixels: np.ndarray = None
    """underlying numpy pixels array"""

    @property
    def image(self) -> Image.Image:
        """
        turn the numpy array into a PIL Image
        """
        image = Image.fromarray(np.rot90(self.pixels), 'RGB')
        return image

    @property
    def width(self) -> int:
        """
        1st dimension of the underlying pixel array
        """
        return self.pixels.shape[0]

    @property
    def height(self) -> int:
        """
        2nd dimension of the underlying pixel array
        """
        return self.pixels.shape[1]

    def prep(
            self,
            pixels: np.ndarray = None,
            loader: Callable[[], np.ndarray] = None,
            **kwargs
    ) -> None:
        """
        provide the source image in a number of ways

        :param pixels: numpy array
        :param loader: function that produces a pixels array
        """

        if pixels is not None:
            self._loader = lambda: pixels

        elif loader is not None:
            self._loader = loader

        else:
            raise Exception("one of pixels or loader must be provided")

    @classmethod
    def from_path(cls, path: str, frame_index: int = 0) -> 'Pierogi':
        """
        :param path: file path to load from
        :param frame_index: if path is a multiframe format (video),
        use this specified frame
        """
        reader = imageio.get_reader(path)
        reader.set_image_index(frame_index)

        def loader():
            return np.rot90(np.array(reader.get_next_data()), axes=(1, 0))

        return cls(loader=loader)

    @classmethod
    def from_shape(cls, shape: tuple) -> 'Pierogi':
        """
        :param shape: (width, height) to make default pixels array
        """

        def loader():
            return np.full((*shape, 3), cls._default_pixel)

        return cls(loader=loader)

    @classmethod
    def from_pil_image(cls, image: Image.Image):
        """
        :param image: PIL Image that has already been loaded
        """

        def loader():
            return np.rot90(np.array(image.convert('RGB')), axes=(1, 0))

        return cls(loader=loader)

    @property
    def pixels(self) -> np.ndarray:
        if self._pixels is None:
            self.load()

        return self._pixels

    def load(self) -> None:
        """
        use the loader return the contained pixels one time
        """
        self._pixels = self._loader()

    def cook(self, pixels: np.ndarray) -> np.ndarray:
        """
        performs actions on a pixel array and returns a cooked array
        """
        return self.pixels

    def show(self) -> None:
        """
        open an image viewer to display the array
        """
        self.image.show()

    def save(self, path: str, optimize: bool = False) -> None:
        """
        save the image to the given path
        """

        output_filename = path
        # if os.path.isdir(path):
        #     output_filename = os.path.join(
        #         path, os.path.split(self.file)[1]
        #     )

        self.image.save(output_filename, optimize=optimize)

    def resize(self, width: int, height: int, resample: int = RESAMPLE):
        """
        resize pixels to new width and height

        :param width: width to resize to

        :param height: height to resize to

        :param resample: resample method to use in Image.resize.
        PIL documentation:

        >    "An optional resampling filter.
        >    This can be one of PIL.Image.NEAREST (use nearest neighbour),
        >    PIL.Image.BILINEAR (linear interpolation),
        >    PIL.Image.BICUBIC (cubic spline interpolation),
        >    or PIL.Image.LANCZOS (a high-quality downsampling filter).
        >    If omitted, or if the image has mode “1” or “P”, it is set PIL.Image.NEAREST."
        """

        self.pixels = np.array(
            Image.fromarray(
                self.pixels
            ).resize(
                (height, width), resample
            )
        )
