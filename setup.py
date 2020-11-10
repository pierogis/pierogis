from setuptools import setup

setup(
    name='pierogis',
    packages=['pierogis'],
    include_package_data=True,
    install_requires=[
        'Pillow',
        'numpy'
    ],
)