import numpy as np

from .ingredient import Ingredient


class MMPX(Ingredient):
    """
    use the MMPX algorithm implemented in rust to scale 2x

    produces interesting style preserving effects for "paletted" pierogis
    """

    def cook(self, pixels: np.ndarray):
        """
        use the binding to the rscolorq package in rust
        to perform an optimization in quantizing and dithering
        """

        from ..algorithms import mmpx
        a = np.full((*pixels.shape[:2], 1), 255)

        # rotating and unrotating because different orientation is expected
        cooked_pixels = mmpx(
            np.ascontiguousarray(np.append(pixels, a, 2), dtype=np.dtype('uint8')),
        )[:, :, :3]

        return cooked_pixels
