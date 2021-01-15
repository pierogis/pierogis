use pyo3::{Python, PyResult};
use pyo3::prelude::{PyModule, pymodule};
use numpy::{PyArray, PyReadonlyArray, Ix1, Ix3, ToPyArray};
use ndarray::parallel::prelude::*;
use rayon::prelude::*;
use rscolorq::{color::Rgb, Matrix2d, Params};

#[pymodule]
fn rpierogis(py: Python<'_>, m: &PyModule) -> PyResult<()> {
    let recipes_module = PyModule::new(py, "recipes")?;
    m.add_submodule(recipes_module)?;

    /// quantize(py_array, palette_size, /)
    /// --
    ///
    /// This function adds two unsigned 64-bit integers.
    #[pyfn(recipes_module, "quantize")]
    fn py_quantize<'py>(
        py: Python<'py>,
        pixels_py_array: PyReadonlyArray<u8, Ix3>,
        palette_size: u8,
    ) -> PyResult<&'py PyArray<u8, Ix3>> {
        let array = pixels_py_array.as_slice()?;

        // let cooked_vec = quantize::cook(array, palette_size);
        // PyArray::from_vec3(py, cooked_vec)

        let shape = pixels_py_array.shape();
        let width = shape[0];
        let height = shape[1];

        // Create the output buffer and quantized palette index buffer
        let mut imgbuf = Vec::with_capacity(width * height * 3);
        let mut quantized_image = Matrix2d::new(width, height);

        // Build the quantization parameters, verify if accepting user input
        let mut conditions = Params::new();
        conditions.palette_size(palette_size);
        conditions.verify_parameters();

        // Convert the input image buffer from Rgb<u8> to Rgb<f64>
        let image = Matrix2d::from_vec(
            array.chunks(3)
                .map(|c| Rgb {
                    red: c[0] as f64 / 255.0,
                    green: c[1] as f64 / 255.0,
                    blue: c[2] as f64 / 255.0,
                })
                .collect(),
            width,
            height,
        );

        let mut palette = Vec::with_capacity(palette_size as usize);

        rscolorq::spatial_color_quant(&image, &mut quantized_image, &mut palette, &conditions);

        // Convert the Rgb<f64> palette to Rgb<u8>
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

        PyArray::from_vec(py, imgbuf).reshape(pixels_py_array.dims())
    }

    #[pyfn(recipes_module, "threshold")]
    fn py_threshold<'py>(
        py: Python<'py>,
        py_array_pixels: &PyArray<u8, Ix3>,
        lower_threshold: u8,
        upper_threshold: u8,
        include_pixel: PyReadonlyArray<i64, Ix1>,
        exclude_pixel: PyReadonlyArray<i64, Ix1>,
    ) -> PyResult<&'py PyArray<u8, Ix3>> {
        let pixels = unsafe { py_array_pixels.as_slice_mut() }?;
        let include_pixel = include_pixel.as_slice()?;
        let exclude_pixel = exclude_pixel.as_slice()?;

        pixels.par_chunks_mut(3)
            .for_each(|pixel_array| -> () {
                // let pixel = Pixel::from(pixel_array);
                let pixel_value = (pixel_array[0] as f64) * 0.299 + (pixel_array[1] as f64) * 0.587 + (pixel_array[2] as f64) * 0.114;
                let replacement =
                    match (pixel_value >= upper_threshold as f64) | (pixel_value <= lower_threshold as f64) {
                        true => &include_pixel,
                        false => &exclude_pixel,
                    };

                // pixel.brightness() >= upper_threshold
                // pixel.replace(replacement)

                pixel_array[0] = replacement[0] as u8;
                pixel_array[1] = replacement[1] as u8;
                pixel_array[2] = replacement[2] as u8;
            });

        pixels.to_pyarray(py).reshape(py_array_pixels.dims())
    }

    // This alternate to the threshold uses ndarrays
    // and was found to be about 3x slower than the slice threshold.
    // I'm keeping it because that was still pretty fast
    // and it's a good example of how to use ndarray and genrows with a pixels PyArray

    // #[pyfn(ingredients_module, "athreshold")]
    // fn py_arraythreshold<'py>(
    //     py: Python<'py>,
    //     array: &PyArray<f64, Ix3>,
    //     upper_threshold: f64,
    //     include_pixel: &PyArray<f64, Ix1>,
    //     exclude_pixel: &PyArray<f64, Ix1>,
    // ) -> PyResult<&'py PyArray<f64, Ix3>> {
    //     let mut array = unsafe { array.as_array_mut() };
    //     let include_pixel = unsafe { include_pixel.as_array_mut() };
    //     let exclude_pixel = unsafe { exclude_pixel.as_array_mut() };
    //
    //     Zip::from(array
    //         .genrows_mut())
    //         .par_apply(|mut pixel| -> () {
    //             let replacement =
    //                 match (pixel[0] * 0.299 + pixel[1] * 0.587 + pixel[2] * 0.114) >= upper_threshold {
    //                     true => &include_pixel,
    //                     false => &exclude_pixel
    //                 };
    //
    //             pixel[0] = replacement[0];
    //             pixel[1] = replacement[1];
    //             pixel[2] = replacement[2];
    //         });
    //
    //     Ok(array.to_pyarray(py))
    // }

    /// rsort(py_array, palette_size, /)
    /// --
    ///
    /// This function adds two unsigned 64-bit integers.
    // #[pyfn(ingredients_module, "sort")]
    // fn sort_py_array<'py>(
    //     py: Python<'py>,
    //     py_array_pixels: &PyArray<f64, Ix3>,
    //     py_array_mask: &PyArray<f64, Ix3>,
    //     upper_threshold: f64,
    // ) -> PyResult<&'py PyArray<f64, Ix3>> {
    //     let mut pixels = unsafe { py_array_pixels.as_slice_mut() }?;
    //
    //     let (width, height, _) = py_array_pixels.shape();
    //
    //     // loop through rows in parallel to generate intervals
    //     // loop through intervals in parallel to sort
    //
    //     for pixel in row {
    //         if pixel
    //     }
    //     intervals.par_apply(|interval| {
    //         interval.par_sort_unstable()
    //     });
    //
    //     pixels.par_chunks_mut(3).collect().par_chunks_mut(height)
    //         .for_each(|row| -> () {
    //             row.for_each(|pixel| {
    //                 if pixel == [255.0, 255.0, 255.0] {
    //                     // add pixel to current interval
    //                     pixel
    //                 }
    //             })
    //             // let pixel = Pixel::from(pixel_array);
    //
    //
    //
    //             let replacement =
    //                 match (pixel_array[0] * 0.299 + pixel_array[1] * 0.587 + pixel_array[2] * 0.114) >= upper_threshold {
    //                     true => &include_pixel,
    //                     false => &exclude_pixel,
    //                 };
    //
    //             // pixel.brightness() >= upper_threshold
    //             // pixel.replace(replacement)
    //
    //             pixel_array[0] = replacement[0];
    //             pixel_array[1] = replacement[1];
    //             pixel_array[2] = replacement[2];
    //         });
    //
    //     println!("{}", py_array.shape()[0]);
    //
    //     pixels.to_pyarray(py).reshape(py_array.dims())
    // }
    Ok(())
}