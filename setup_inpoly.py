# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 16:47:44 2015

@author: Steven.Ettema
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
    name = 'Inpoly App',
    ext_modules = cythonize("C:\Users\steven.ettema\Documents\GitHub\FVTools\in_poly_c.pyx"),
    include_dirs=[numpy.get_include()]
)