use rscolorq::{FilterSize, Matrix2d, Params};
use rscolorq::color::Rgb;

#[allow(clippy::too_many_arguments)]
pub fn cook(
    pixels_array: &&[u8],
    width: usize,
    height: usize,
    colors: &&[u8],
    palette_size: u8,
    iters_per_level: usize,
    repeats_per_temp: usize,
    initial_temp: f64,
    final_temp: f64,
    filter_size: u8,
    dithering_level: f64,
    seed: Option<u64>,
) -> Vec<u8> {
    // Build the quantization parameters, verify if accepting user input
    let mut conditions = Params::new();

    // set parameters for quantization
    conditions.palette_size(palette_size);
    conditions.dithering_level(dithering_level);

    conditions.filter_size(match filter_size {
        1 => FilterSize::One,
        3 => FilterSize::Three,
        5 => FilterSize::Five,
        _ => panic!("Filter size must be 1, 3, or 5"),
    });

    conditions.seed(seed);

    conditions.initial_temp(initial_temp);
    conditions.final_temp(final_temp);
    conditions.iters_per_level(iters_per_level);
    conditions.repeats_per_temp(repeats_per_temp);

    // verify
    conditions.verify_parameters().unwrap();

    // Create the output buffer and quantized palette index buffer
    let mut imgbuf = Vec::with_capacity(width * height * 3);
    // height, width to account for different input orientation (w x h)
    let mut quantized_image = Matrix2d::new(height, width);

    // Convert the input array buffer from chunks of <u8> to Rgb<f64>
    // println!("numpy array: {}", array[3]);
    let image = Matrix2d::from_vec(
        pixels_array
            .chunks(3)
            .map(|c| Rgb {
                red: c[0] as f64 / 255.0,
                green: c[1] as f64 / 255.0,
                blue: c[2] as f64 / 255.0,
            })
            .collect(),
        height, // note these are switched, numpy is using (width, height, 3)
        width,  // where this lib expects (height, width, 3)
    );

    if colors.len() >= 3 {
        // map colors slice to Vec<Rgb>
        let colors = colors.chunks(3).map(|c| {
            Rgb {
                red: c[0] as f64 / 255.0,
                green: c[1] as f64 / 255.0,
                blue: c[2] as f64 / 255.0,
            }
        })
            .collect::<Vec<Rgb>>();

        // use this Vec in the conditions for dithering
        conditions.palette(colors).unwrap();
    }

    // also create a palette for the outcome of the algorithm
    let mut palette = Vec::with_capacity(palette_size as usize);

    // perform the quantization, filling these refs
    rscolorq::spatial_color_quant(&image, &mut quantized_image, &mut palette, &conditions).unwrap();

    // convert the Rgb<f64> palette to Rgb<u8>
    let palette = palette
        .iter()
        .map(|&c| {
            let color = 255.0 * c;
            [
                color.red.round() as u8,
                color.green.round() as u8,
                color.blue.round() as u8,
            ]
        })
        .collect::<Vec<[u8; 3]>>();

    // Create the final image by color lookup from the palette
    quantized_image.iter().for_each(|&c| {
        imgbuf.extend_from_slice(&*palette.get(c as usize).unwrap());
    });

    imgbuf
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
