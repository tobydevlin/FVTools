# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 16:52:16 2015

@author: Steven.Ettema
"""

import numpy as np
#import matplotlib.path as mplPath
#
#def in_poly(px,py,xy,face):
#    #Setup an empty matrix for the data
#    datv= np.empty((len(px),1))
#    datv[:] = np.NAN
#    for aa in range(len(face)):
#        #builds it polygon by polygon
#        poly = np.vstack((xy[face[aa,0]],xy[face[aa,1]],xy[face[aa,2]],xy[face[aa,3]]))
#        bbPath = mplPath.Path(poly)
#        #checks if the data is contained within the polygon built in that timestep
#        tt=bbPath.contains_points(np.transpose(np.vstack((px,py))))
#        datv[tt]=aa
#        
#        
        
#
#//  Globals which should be set before calling this function:
#//
#//  int    polyCorners  =  how many corners the polygon has (no repeats)
#//  float  polyX[]      =  horizontal coordinates of corners
#//  float  polyY[]      =  vertical coordinates of corners
#//  float  x, y         =  point to be tested
#//
#//  (Globals are used in this example for purposes of speed.  Change as
#//  desired.)
#//
#//  The function will return YES if the point x,y is inside the polygon, or
#//  NO if it is not.  If the point is exactly on the edge of the polygon,
#//  then the function may return YES or NO.
#//
#//  Note that division by zero is avoided because the division is protected
#//  by the "if" clause which surrounds it.

def in_poly(px, py, xy, face):
    face=np.ndarray.astype(face,int)
    out2= np.repeat(np.nan,len(px))
    
    for bb in range(0,len(px)):
        x=px[bb]
        y=py[bb]
        for aa in range(0,len(face)):
            polyX=xy[face[aa,:],0]
            polyY=xy[face[aa,:],1]
            polyX=polyX.tolist()
            polyY=polyY.tolist()
            polyCorners=len(polyY)  #place a check if is a tri
            i = int(0)
            j = int(polyCorners-1)
            out = False     #vectorise this into a bool array to remove the bb loop
            
            for i in range(0,(polyCorners-1)):
                if (((polyY[i]< y) & (polyY[j]>=y))
                | ((polyY[j]< y) & (polyY[i]>=y))
                & ((polyX[i]<=x) | (polyX[j]<=x))):
                   
                    if (polyX[i]+(y-polyY[i])/(polyY[j]-polyY[i])*(polyX[j]-polyX[i])<x):
                        out= not out
                j=i;
                #if multiple points ar found to be in the same poly then preference is given to the last poly
            if out==True:
                out2[bb]=aa
    return out2
    

#px=np.array([0, 0.5, 1.5, 2])
#py=np.array([0, 0.5, 0.5, 3])
#face=np.array([[0, 1, 3, 2],[ 2, 3, 5, 4]])
#xy=np.array([[0.0, 0.0],[0, 1],[1, 0],[1, 1],[2, 0],[2,1]])
#
#t=in_poly(px,py,xy,face)