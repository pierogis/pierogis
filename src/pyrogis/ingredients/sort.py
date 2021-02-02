import numpy as np

from .ingredient import Ingredient
from .rotate import Rotate
from .seasonings import Seasoning, Threshold


class Sort(Ingredient):
    """
    Sort a pixel array
    Uses its mask to determine which groups of pixels to sort (white pixels get sorted)

    Can use a seasoning to create that mask when cooking, or have it preloaded using a season method
    """

    def prep(self, rotate: Rotate = None, seasoning: Seasoning = Threshold(),
             delimiter: np.ndarray = np.array([255, 255, 255]), **kwargs):
        """
        :param rotate: define the direction to rotate on. cook sorts from bottom to top after rotation, then unrotates
        :param seasoning: create a mask from a seasoning
        :param delimiter: the pixel that should be used as the sort subgroup delimiter

        Extra kwargs get passed to the Rotate if one is not provided
        """
        self.delimiter = delimiter

        if rotate is None:
            rotate = Rotate(**kwargs)

        self.rotate = rotate

        # apply seasoning as mask if provided
        self.seasoning = seasoning

    def cook(self, pixels: np.ndarray):
        """
        Sort within each sequence group of contiguous white pixels in the mask (may be all white)
        """
        # rotate self.mask and pixels to correspond to self.angle
        rotate = self.rotate

        if self.mask is None:
            self.seasoning.target = Ingredient(pixels)
            self.seasoning.season(self)

        rotated_mask = rotate.cook(self.mask)
        rotated_pixels = rotate.cook(pixels)

        # false indicates that the pixel should not be sorted
        boolean_array = np.all(rotated_mask == self._white_pixel, axis=2)

        sorted_pixels = rotated_pixels
        # loop through one axis
        for i in range(rotated_pixels.shape[0]):
            # get that axis
            axis = rotated_pixels[i]
            # and the axis for the mask-truth
            boolean_axis = boolean_array[i]
            # get the indices for this row on the mask that are True
            masked_indices_axis = np.nonzero(boolean_axis)[0]
            # split up the axis into sub groups at the indices where the mask is inactive
            sort_groups = np.split(axis, masked_indices_axis)

            sorted_groups = []
            # loop through the groups
            for group in sort_groups:
                # np.sort(group)
                # if the subgroup to be sorted contains no pixels or just one pixel, ignore
                if group.size > 3:
                    # intensity as the sorting criterion
                    intensities = np.average(group, axis=1)
                    # get "sort order" indices of the intensities of this group
                    indices = np.argsort(intensities)
                    # sort the group by these indices
                    group = group[indices]
                sorted_groups.append(group)

            # concatenate the row back together, sorted in the mask
            sorted_pixels[i] = np.concatenate(sorted_groups)

        # unrotate sorted_pixels to return to correct orientation
        unrotate = Rotate.unrotate(rotate)
        sorted_pixels = unrotate.cook(sorted_pixels)

        return sorted_pixels

    @classmethod
    def add_parser_arguments(cls, parser):
        parser.add_argument('-t', '--turns', default=0, type=int)
        Threshold.add_parser_arguments(parser)
