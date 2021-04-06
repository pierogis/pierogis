from setuptools import find_packages
from setuptools import setup
from setuptools_rust import RustExtension, Binding

readme = open("README.md").read()
changelog = open("CHANGELOG.md").read()

setup(
    name='pyrogis',
    author="pierogis-live",
    author_email="admin@pierogis.live",
    description="image processing framework",
    url="https://github.com/pierogis/pierogis",
    long_description=readme + "\n\n" + changelog,
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
        'rich>=9.11.0'
    ],
    extra_requires={
        'dev': [
            'setuptools-scm', 'setuptools-rust'
        ]
    },
    rust_extensions=[
        RustExtension("pierogis_rs", binding=Binding.PyO3)
    ],
    entry_points={
        'console_scripts': [
            "pyrogis=pyrogis.__main__:main"
        ]
    },
    zip_safe=False
)
