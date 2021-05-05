use image::{DynamicImage, RgbaImage, RgbImage};
use ndarray::parallel::prelude::*;
use numpy::{Ix1, Ix2, Ix3, PyArray, PyReadonlyArray, ToPyArray};
use pyo3::{PyResult, Python};
use pyo3::prelude::{pymodule, PyModule};
use rayon::prelude::*;

use crate::quantize;

#[pymodule]
fn algorithms(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    /// quantize(py_array, palette_size, /)
    /// --
    ///
    /// quantize an image as a numpy array using rscolorq.
    #[pyfn(m, "quantize")]
    #[allow(clippy::too_many_arguments)]
    fn py_quantize<'py>(
        py: Python<'py>,
        pixels_py_array: PyReadonlyArray<u8, Ix3>,
        palette_py_array: PyReadonlyArray<u8, Ix2>,
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
        let palette = palette_py_array.as_slice()?;

        let shape = pixels_py_array.shape();
        let width = shape[0];
        let height = shape[1];

        let cooked_array = quantize::cook(
            &array,
            width,
            height,
            &palette,
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

    #[pyfn(m, "threshold")]
    #[allow(clippy::too_many_arguments)]
    fn py_threshold<'py>(
        py: Python<'py>,
        pixels_py_array: &PyArray<u8, Ix3>,
        lower_threshold: u8,
        upper_threshold: u8,
        include_pixel: PyReadonlyArray<u8, Ix1>,
        exclude_pixel: PyReadonlyArray<u8, Ix1>,
        inner: bool,
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
            let included: bool = if inner {
                (pixel_value <= upper_threshold as f64)
                    & (pixel_value >= lower_threshold as f64)
            } else {
                (pixel_value >= upper_threshold as f64)
                    | (pixel_value <= lower_threshold as f64)
            };

            let replacement = match included
            {
                true => &include_pixel,
                false => &exclude_pixel,
            };

            // replace rgb on the current chunk
            pixel_array[0] = replacement[0] as u8;
            pixel_array[1] = replacement[1] as u8;
            pixel_array[2] = replacement[2] as u8;
        });

        pixels.to_pyarray(py).reshape(pixels_py_array.dims())
    }

    #[pyfn(m, "mmpx")]
    #[allow(clippy::too_many_arguments)]
    fn py_mmpx<'py>(
        py: Python<'py>,
        pixels_py_array: &PyArray<u8, Ix3>,
    ) -> PyResult<&'py PyArray<u8, Ix3>> {
        let pixels = pixels_py_array.to_vec().unwrap();
        let shape = pixels_py_array.shape();
        let width = shape[0];
        let height = shape[1];

        let image = RgbaImage::from_raw(
            height as u32, width as u32, pixels,
        ).unwrap();

        mmpx::magnify(&image)
            .to_pyarray(py)
            .reshape((width * 2, height * 2, 4))
    }

    Ok(())
}