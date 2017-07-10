# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 15:08:45 2015

@author: toby.devlin
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
    name='Dave App',
    ext_modules=cythonize("C:\Users\steven.ettema\Desktop\python_dev\proto\dave_c.pyx"),
    include_dirs=[numpy.get_include()]
)