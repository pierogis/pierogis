import numpy as np

from pierogis.ingredients.ingredient import Ingredient


class Sort(Ingredient):

    def prep(self, **kwargs):
        self.target = kwargs.get('target')
        self.delimiter = kwargs.get('delimiter', np.array([255, 255, 255]))

    def cook(self, pixels: np.ndarray):
        """
        Sort within each sequence group of contiguous white pixels in the mask (may be all white)

        NOT WORKING
        """
        mask = self.mask
        # false indicates that the pixel should not be sorted
        boolean_array = np.all(mask == self._white_pixel, axis=2)

        sorted_pixels = pixels
        # loop through one axis
        for i in range(pixels.shape[0]):
            # get that axis
            axis = pixels[i]
            # and the axis for the mask-truth
            boolean_axis = boolean_array[i]
            # get the indices for this row on the mask that are True
            masked_indices_axis = np.nonzero(np.invert(boolean_axis))[0]
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

        return sorted_pixels
