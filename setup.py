from setuptools import setup
from setuptools import find_packages

setup(
    name='pierogis',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'Pillow>=8.0.1',
        'numpy>=1.19.4'
    ],
    entry_points={
        'console_scripts': [
            "pierogis=pierogis.__main__:main"
        ]
    }
)
