import numpy as np
import tensorflow as tf
import tensorflow_hub

from .ingredient import Ingredient
from .pierogi import Pierogi


class Style(Ingredient):
    stylization_module = tensorflow_hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

    def prep(self, pierogi: Pierogi, **kwargs):
        """
        :param pierogi: Pierogi to use as style
        """
        self.style = pierogi

    def cook(self, pixels: np.ndarray):
        content_pixels = pixels.astype(np.float32)[np.newaxis, ...] / 255.
        style_pixels = self.style.pixels.astype(np.float32)[np.newaxis, ...] / 255.

        style_pixels = tf.image.resize(style_pixels, (256, 256))

        outputs = self.stylization_module(tf.constant(content_pixels), tf.constant(style_pixels))
        stylized_pixels = np.squeeze(np.asarray(outputs[0] * 255, dtype='uint8'))

        return stylized_pixels
