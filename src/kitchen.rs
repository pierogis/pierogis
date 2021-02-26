use pyo3::{Python, PyResult, PyAny};
use pyo3::types::IntoPyDict;
use std::thread;


#[pyclass]
pub struct Kitchen {
    chef_type: PyAny,
}

#[pymethods]
impl Kitchen {
    #[new]
     fn __new__(obj: &PyRawObject, chef_type: PyAny) -> PyResult<()> {
         obj.init({
             Kitchen {
                 chef_type,
             }
         })
     }

    fn cook_dish_descs(&self, dish_descriptions: Vec<PyAny>) -> PyResult<(Vec<PyAny>)> {
        x: Vec<PyAny>;
        let chef_type = self.chef_type;
        Python::with_gil(|py| {
            py.allow_threads(|| {
                x = dish_descriptions.into_iter()
                    .map(|dish_description| {
                        thread::spawn(move || {
                            let kwargs = [
                                ("Chef", chef_type),
                                ("dish_desc", dish_description)
                            ].into_py_dict(py);
                            let chef = chef_type.call();
                            let dish = chef.call_method(py, "cook_dish_desc", (), Some(kwargs)).unwrap();

                            dish
                        })
                    }).collect::<Vec<PyAny>>();
            });
        });

        x
    }
}
