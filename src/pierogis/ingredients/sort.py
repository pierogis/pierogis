import numpy as np

from pierogis.ingredients.ingredient import Ingredient

class Sort(Ingredient):

    def prep(self, **kwargs):
        self.target = kwargs.get('target')
        self.delimiter = kwargs.get('delimiter', np.array([255, 255, 255]))

    # def cook(self, pixels: np.ndarray):
    #     mask = self.mask
    #     boolean_array = np.all(mask == self._white_pixel, axis=2)
    #
    #     # false indicates that the pixel should not be sorted
    #
    #     intensities = np.average(pixels, axis=2)
    #     indices = np.argsort(intensities)
    #
    #     sorted_pixels = pixels[np.arange(len(pixels))[:, np.newaxis], indices]
    #
    #     return sorted_pixels

    def cook(self, pixels: np.ndarray):
        """
        Sort within each sequence group of contiguous white pixels in the mask (may be all white)

        NOT WORKING
        """
        mask = self.mask
        boolean_array = np.all(mask == self._white_pixel, axis=2)
        # false indicates that the pixel should not be sorted

        # recursive sort
        # find the index of the first false along the sort axis for each off axis
        # color all after this index black
        # set first from i= 0 j= first i
        # for each consecutive i j in the splits
        #   row[0:i] = white
        #   row[i:j] = pixels
        #   row{j:] = black
        #   crop the left to the lowest non white index
        #   crop the right to the highest black index
        #   cook these pixels with a new sort
        # "terminating condition" is that there is no mask
        # create a sort of each set of pixels

        intensities = np.average(pixels, axis=2)
        start = 0
        end = 3
        j = 0
        ind = np.array([[0]])
        a = intensities[ind]
        intensities[ind] = np.sort(intensities[ind])

        indices = np.argsort(intensities)

        sorted_pixels = pixels[np.arange(len(pixels))[:, np.newaxis], indices]

        return sorted_pixels