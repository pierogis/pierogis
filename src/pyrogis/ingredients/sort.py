from typing import List

import numpy as np

from .ingredient import Ingredient
from .pierogi import Pierogi
from .rotate import Rotate
from .seasonings import Seasoning, Threshold


class Sort(Ingredient):
    """
    sort a pixel array

    uses its mask to determine which groups of pixels to sort
    (white pixels get sorted)

    can use a seasoning to create that mask when cooking,
    or have it preloaded using a season method
    """

    def prep(
            self, rotate: Rotate = None,
            delimiter: np.ndarray = np.array([255, 255, 255]),
            **kwargs
    ):
        """
        cook sorts from bottom to top after rotation, then unrotates
        extra kwargs get passed to the Rotate if one is not provided

        :param rotate: define the direction to rotate on
        :param seasoning: create a mask from a seasoning
        :param delimiter: pixel used as the sort subgroup delimiter
        :param target: pierogi to use as target for an automatic seasoning
        """
        self.delimiter = delimiter

        if rotate is None:
            rotate = Rotate(turns=0)

        self.rotate = rotate

    def cook(self, pixels: np.ndarray):
        """
        sort within each sequence group of contiguous white pixels
        in the mask (may be all white)
        """
        # rotate self.mask and pixels to correspond to self.angle
        rotate = self.rotate

        mask = self.mask_pixels(pixels)

        rotated_mask = rotate.cook(mask)
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
            # split up the axis into sub groups at indices where mask is black
            sort_groups = np.split(axis, masked_indices_axis)

            sorted_groups = []
            # loop through the groups
            for group in sort_groups:
                # np.sort(group)
                # if the subgroup to be sorted contains 0 or 1 pixels, ignore
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
