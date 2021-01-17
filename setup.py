from setuptools import setup
from setuptools import find_packages
from setuptools_rust import RustExtension, Binding

setup(
    name='pyrogis',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'Pillow>=8.0.1',
        'numpy>=1.19.4'
    ],
    rust_extensions=[
        RustExtension("rpierogis", binding=Binding.PyO3)
    ],
    entry_points={
        'console_scripts': [
            "pierogis=pyrogis.__main__:main"
        ]
    },
    zip_safe=False
)
