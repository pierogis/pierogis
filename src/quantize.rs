use ndarray::ArrayView3;
use itertools::Itertools;

pub fn cook(pixels: &[f64], palette_size: u8) -> Vec<u8> {

}

// NOTES on spatial quantization

// COLOR PERCEPTION
// There is a notion of the neighborhood N_ik that points to other pixels j
// i,j represents the pixel indices in the flattened pixel grid - i is x and y
// In the paper the pixels are indexed scanning rows left to right, then moving down the row (raster scan order)
// k represents the 1,2,3 index in rgb or any color system (3tuple)

// There is also a kernel function W that uses the relative location (distance?) of i and j
// to create a 3tuple of "perception filter" weights for those pixel indicies -> w_ijk

// With the pixel defined as x_j, the sum of the elementwise product of weights 3tuple w_ij and pixel 3tuple (rgb) x_j
// for those j in the neighborhood of i is a general definition of the perceived color of pixel at i
// subject to the kernel function that is being used to specify perceieved value of color

// The weights w_ij for pixel-i's neighborhood should sum to 1
// In the paper they used w_ij = exp(-euclidean distance between two pixels at i and j / a variance)

// COST FUNCTION
// There is a set of 3tuple colors Y that constitute a palette. y_v is vth color in the palette
// M is a 2d boolean array, M_iv being 1 means that pixel at i is quantized to color at v
// The sum of each pixel's ((before vs after-quantization filtered 3tuple euclidean distance)) is the cost
// The optimization problem is finding the combination of colors (Y) and assignements (M) that minimizes cost

