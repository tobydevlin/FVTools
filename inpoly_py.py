# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 16:08:28 2015

defines which voly a vector of points is in



@author: Steven.Ettema
"""
import ctypes as ct
import numpy as np


def inpoly_py(px, py, dat_x, dat_y):

    # Load Library
    lib = ct.cdll.LoadLibrary('in_poly.dll')  # This Doesn't Work as is on Steven's Drive

    # Convert to C++ type
    px = px.astype(ct.c_double)
    py = py.astype(ct.c_double)
    dat_x = dat_x.astype(ct.c_double)
    dat_y = dat_y.astype(ct.c_double)
    n_poly = ct.c_int(np.size(dat_x, 0))
    polyCorners = ct.c_int(np.size(dat_x, 1))
    n_points = ct.c_int(np.size(px, 0))

    # Convert to C++ Pointer
    x_p = dat_x.ctypes.data_as(ct.POINTER(ct.c_double))
    y_p = dat_y.ctypes.data_as(ct.POINTER(ct.c_double))
    px_p = px.ctypes.data_as(ct.POINTER(ct.c_double))
    py_p = py.ctypes.data_as(ct.POINTER(ct.c_double))

    # Set Function Input/Output
    lib.inpoly.restype = np.ctypeslib.ndpointer(dtype=ct.c_int, shape=(np.size(px, 0),))
    lib.inpoly.argtypes = [ct.POINTER(ct.c_double),
                           ct.POINTER(ct.c_double),
                           ct.POINTER(ct.c_double),
                           ct.POINTER(ct.c_double),
                           ct.c_int,
                           ct.c_int]

    return lib.inpoly(px_p, py_p, x_p, y_p, n_poly, polyCorners, n_points)