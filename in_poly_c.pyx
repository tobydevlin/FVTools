# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 16:52:16 2015

@author: Steven.Ettema
"""
import numpy as np
cimport numpy as np
#import matplotlib.path as mplPath
DTYPE1=np.int
DTYPE2=np.float

ctypedef np.int_t DTYPE1_t
ctypedef np.float_t DTYPE2_t

    

def in_poly(px, py, xy, face):
    assert px.dtype == DTYPE2 and py.dtype == DTYPE2
    assert xy.dtype == DTYPE2
    assert face.dtype == DTYPE1
    cdef int i, j, aa, bb, x, y
    cdef bint out
    cdef np.ndarray out2 = np.repeat(np.nan,len(px), dtype=DTYPE1)
    cdef np.ndarray polyX = np.repeat(np.nan,len(face[0,:]), dtype=DTYPE2)  
    cdef np.ndarray polyY = np.repeat(np.nan,len(face[0,:]), dtype=DTYPE2)
 
    
    for bb in range(0,len(px)):
        x=px[bb]
        y=py[bb]
        for aa in range(0,len(face)):
            polyX=xy[face[aa,:],0]
            polyY=xy[face[aa,:],1]
            polyCorners=len(polyY)  #place a check if is a tri
            i = 0
            j = int(polyCorners-1)
            out = 0
            
            for i in range(0,(polyCorners-1)):
                if (((polyY[i]< y) & (polyY[j]>=y))
                | ((polyY[j]< y) & (polyY[i]>=y))
                & ((polyX[i]<=x) | (polyX[j]<=x))):
                   
                    if (polyX[i]+(y-polyY[i])/(polyY[j]-polyY[i])*(polyX[j]-polyX[i])<x):
                        out=~out
                j=i;
                #if multiple points ar found to be in the same poly then preference is given to the last poly
            if out==~0:
                out2[bb]=aa
    return out2
    

#px=np.array([0, 0.5, 1.5, 2])
#py=np.array([0, 0.5, 0.5, 3])
#face=np.array([[0, 1, 3, 2],[ 2, 3, 5, 4]])
#xy=np.array([[0.0, 0.0],[0, 1],[1, 0],[1, 1],[2, 0],[2,1]])
#
#t=in_poly(px,py,xy,face)