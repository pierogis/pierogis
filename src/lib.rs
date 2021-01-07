use ndarray::{ArrayD, ArrayViewD, ArrayViewMutD};
use numpy::{IntoPyArray, PyArray, Ix3, PyReadonlyArrayDyn, ToPyArray};
use pyo3::prelude::{pymodule, PyModule, PyResult, Python};

#[pymodule]
fn rpierogis(py: Python<'_>, m: &PyModule) -> PyResult<()> {
    let quantize_module = PyModule::new(py, "quantize")?;
    m.add_submodule(quantize_module)?;

    // immutable example
    fn axpy(a: f64, x: ArrayViewD<'_, f64>, y: ArrayViewD<'_, f64>) -> ArrayD<f64> {
        a * &x + &y
    }

    // mutable example (no return)
    fn mult(a: f64, mut x: ArrayViewMutD<'_, f64>) {
        x *= a;
    }

    // wrapper of `axpy`
    #[pyfn(m, "axpy")]
    fn axpy_py<'py>(
        py: Python<'py>,
        a: f64,
        x: PyReadonlyArrayDyn<f64>,
        y: PyReadonlyArrayDyn<f64>,
    ) -> &'py PyArrayDyn<f64> {
        let x = x.as_array();
        let y = y.as_array();
        axpy(a, x, y).into_pyarray(py)
    }

    // wrapper of `mult`
    #[pyfn(m, "mult")]
    fn mult_py(_py: Python<'_>, a: f64, x: &PyArrayDyn<f64>) -> PyResult<()> {
        let x = unsafe { x.as_array_mut() };
        mult(a, x);
        Ok(())
    }

    #[pyfn(quantize_module, "quantize")]
    fn rquantize<'py>(py: Python<'py>, py_array: &PyArray<u8, Ix3>, palette_size: u8) -> &'py PyArray<u8, Ix3> {
        use quantize::quantize;

        let array = unsafe { py_array.as_array() };

        let cooked_vec = quantize(array, palette_size);

        PyArray::from_vec3(py, cooked_vec)
    }

    Ok(())
}