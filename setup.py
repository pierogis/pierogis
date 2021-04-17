import os

from setuptools import find_packages
from setuptools import setup

readme = open("README.md").read()

setup_requires = [
    'setuptools-scm>=6.0.1', 'setuptools-rust', 'wheel'
]

if not os.environ.get('READTHEDOCS'):
    from setuptools_rust import RustExtension, Binding

    rust_extensions = [
        RustExtension("pierogis_rs", binding=Binding.PyO3)
    ]
else:
    # don't use RustExtensions
    rust_extensions = None

setup(
    name='pyrogis',
    author="pierogis-live",
    author_email="admin@pierogis.live",
    description="image and animation processing framework",
    url="https://github.com/pierogis/pierogis",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'Pillow>=8.0.1',
        'numpy>=1.20.1',
        'imageio>=2.9.0',
        'imageio-ffmpeg>=0.4.3',
        'natsort>=7.1.1',
        'rich>=10.1.0'
    ],
    setup_requires=setup_requires,
    extras_require={
        'dev': setup_requires + ['pytest']
    },
    rust_extensions=rust_extensions,
    entry_points={
        'console_scripts': [
            "pyrogis=pyrogis.__main__:main"
        ]
    },
    zip_safe=False
)
