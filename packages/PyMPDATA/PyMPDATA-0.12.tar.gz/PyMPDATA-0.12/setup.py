"""
the magick behind ``pip install ...``
"""
import os
from setuptools import setup, find_packages


def get_long_description():
    """returns contents of README.md file"""
    with open("README.md", "r", encoding="utf8") as file:
        long_description = file.read()
    return long_description


setup(
    name='PyMPDATA',
    description='Numba-accelerated Pythonic implementation of MPDATA '
                'with examples in Python, Julia and Matlab',
    version='0.12',
    setup_requires=['setuptools_scm'],
    install_requires=[
        'numba' + ('==0.55.0' if 'CI' in os.environ else ''),
        'numpy' + ('==1.21' if 'CI' in os.environ else ''),
        'pystrict'
    ],
    author='https://github.com/atmos-cloud-sim-uj/PyMPDATA/graphs/contributors',
    author_email='sylwester.arabas@uj.edu.pl',
    license="GPL-3.0",
    packages=find_packages(include=['PyMPDATA', 'PyMPDATA.*']),
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development :: Libraries'
    ],
    keywords='atmospheric-modelling, numba, numerical-integration, '
             'advection, pde-solver, advection-diffusion'
)
