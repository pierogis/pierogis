use pyo3::{Python, PyResult, PyAny};
use pyo3::types::IntoPyDict;
use std::thread;

#[pyclass]
pub struct Kitchen {
    chef_type: PyAny,
}


// Kitchen is a pyobj shared from Rust
// it can be used by the wasm module and by python cli

// It gets a series of dish descriptions and uses its chefs

// rust should take many input dish description and cook each
// python should dump into frames and create a list of dish descriptions
// rust should do a chef.cook_dish_desc for each

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
