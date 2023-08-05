from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import numpy as np

# Use the README.md file as description
with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name='mylibq23452352345',
    version='0.0.1',
    packages=find_packages(),
    author='Ron Cheong',
    description='Some description here',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_dirs=np.get_include(),
    install_requires=[
        'numpy>=1.19.2',
        'PyObjC;platform_system=="Darwin"',
        'PyGObject;platform_system=="Linux"',
    ],
    ext_modules=cythonize([
        Extension('lib.test', ['lib/test.pyx'])
    ])
)