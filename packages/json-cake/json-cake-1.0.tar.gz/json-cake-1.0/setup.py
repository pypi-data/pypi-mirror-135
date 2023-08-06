from setuptools import setup
import setuptools


description = 'A Simple JSON Helper Package'
long_description = 'A Simple JSON Helper Package, Created By Jaasim, More Info @ Readme.md'

setup(
    name='json-cake',
    version='1.0',
    author='Jaasim',
    author_email='jaasim2008@gmail.com',
    description='Simple JSON Accessing Module',
    long_description=long_description,
    keywords=['JSON', 'Easy JSON', 'JSON Packaging'],
    python_requires='>=3.9',
    py_modules=['json-cake'],
    package_dir={'': 'src'}
)
