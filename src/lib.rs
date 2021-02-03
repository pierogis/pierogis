use ndarray::parallel::prelude::*;
use numpy::{Ix1, Ix3, PyArray, PyReadonlyArray, ToPyArray};
use pyo3::prelude::{pymodule, PyModule};
use pyo3::{PyResult, Python};
use rayon::prelude::*;

mod quantize;

#[pymodule]
fn rpierogis(py: Python<'_>, m: &PyModule) -> PyResult<()> {
    let recipes_module = PyModule::new(py, "recipes")?;
    m.add_submodule(recipes_module)?;

    /// quantize(py_array, palette_size, /)
    /// --
    ///
    /// This function adds two unsigned 64-bit integers.
    #[pyfn(recipes_module, "quantize")]
    #[allow(clippy::too_many_arguments)]
    fn py_quantize<'py>(
        py: Python<'py>,
        pixels_py_array: PyReadonlyArray<u8, Ix3>,
        palette_size: u8,
        iters_per_level: usize,
        repeats_per_temp: usize,
        initial_temp: f64,
        final_temp: f64,
        filter_size: u8,
        dithering_level: f64,
        seed: Option<u64>,
    ) -> PyResult<&'py PyArray<u8, Ix3>> {
        let array = pixels_py_array.as_slice()?;

        let shape = pixels_py_array.shape();
        let width = shape[0];
        let height = shape[1];

        let cooked_array = quantize::cook(
            &array,
            width,
            height,
            palette_size,
            iters_per_level,
            repeats_per_temp,
            initial_temp,
            final_temp,
            filter_size,
            dithering_level,
            seed,
        );

        // return a py array resized to the input shape
        PyArray::from_vec(py, cooked_array).reshape((width, height, 3))
    }

    #[pyfn(recipes_module, "threshold")]
    #[allow(clippy::too_many_arguments)]
    fn py_threshold<'py>(
        py: Python<'py>,
        pixels_py_array: &PyArray<u8, Ix3>,
        lower_threshold: u8,
        upper_threshold: u8,
        include_pixel: PyReadonlyArray<i64, Ix1>,
        exclude_pixel: PyReadonlyArray<i64, Ix1>,
    ) -> PyResult<&'py PyArray<u8, Ix3>> {
        let pixels = unsafe { pixels_py_array.as_slice_mut() }?;
        let include_pixel = include_pixel.as_slice()?;
        let exclude_pixel = exclude_pixel.as_slice()?;

        // iterate through the flat array in chunks of 3
        pixels.par_chunks_mut(3).for_each(|pixel_array| {
            // get the brightness of the pixel
            let pixel_value = (pixel_array[0] as f64) * 0.299
                + (pixel_array[1] as f64) * 0.587
                + (pixel_array[2] as f64) * 0.114;
            // get with the correct pixel based on if it is outside a threshold
            let replacement = match (pixel_value >= upper_threshold as f64)
                | (pixel_value <= lower_threshold as f64)
            {
                true => &include_pixel,
                false => &exclude_pixel,
            };

            // pixel.brightness() >= upper_threshold
            // pixel.replace(replacement)

            // replace rgb on the current chunk
            pixel_array[0] = replacement[0] as u8;
            pixel_array[1] = replacement[1] as u8;
            pixel_array[2] = replacement[2] as u8;
        });

        pixels.to_pyarray(py).reshape(pixels_py_array.dims())
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
