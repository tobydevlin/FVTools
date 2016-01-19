# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 16:08:28 2015

defines which voly a vector of points is in



@author: Steven.Ettema
"""
import ctypes as ct
import numpy as np
#import matplotlib.path as mplPath
#import time as time
#from netCDF4 import Dataset


def inpoly_py(px,py,dat_x,dat_y):
    mydll=ct.cdll.LoadLibrary('C:\\Users\\steven.ettema\\Documents\\Visual Studio 2015\\Projects\\in_poly\\x64\\Release\\in_poly.dll')
    mycfun=mydll.inpoly
    px=px.astype(ct.c_double)
    py=py.astype(ct.c_double)
    n_poly=np.size(dat_x,0)
    polyCorners=np.size(dat_x,1)
    dat_x=dat_x.astype(ct.c_double)
    dat_y=dat_y.astype(ct.c_double)    

#set up pointers to the data - use by ref in future
    pnt_x=dat_x.ctypes.data_as(ct.POINTER(ct.c_double))
    pnt_y=dat_y.ctypes.data_as(ct.POINTER(ct.c_double))
    pnt_px=px.ctypes.data_as(ct.POINTER(ct.c_double))
    pnt_py=py.ctypes.data_as(ct.POINTER(ct.c_double))
#get some sizes to preallocate memory in c++
    n_points=np.size(px,0)
#just some input/ output checks    
    mycfun.restype = np.ctypeslib.ndpointer(dtype=ct.c_int,shape=(n_points,))
    mycfun.argtypes=[ct.POINTER(ct.c_double),
                ct.POINTER(ct.c_double), 
              ct.POINTER(ct.c_double),
             ct.POINTER(ct.c_double),
            ct.c_int,
           ct.c_int]
    
                 
    out = mycfun(pnt_px,pnt_py,pnt_x,pnt_y,ct.c_int(n_poly),ct.c_int(polyCorners),ct.c_int(n_points))


    return out


#def inpoly_old(px,py,dat_x,dat_y):#face,xy):
#    datv=np.empty(len(px))    
#    datv[:]=np.nan
#    pts=np.transpose(np.vstack([px,py]))
#    for aa in range(len(dat_x)):
#        #poly = np.array((xy[face[aa,0]],xy[face[aa,1]],xy[face[aa,2]],xy[face[aa,3]]))
#        poly = np.array([dat_x[aa,:],dat_y[aa,:]])
#        bbPath = mplPath.Path(poly.transpose())
#        t=bbPath.contains_points(pts)
#        datv[t]=aa
#    return datv
#    
#    
###############################TESTING#####################################
##px=np.array([-0.5,2.5])
##py=np.array([0.5,0.5])
##dat_x=np.array([[0,0,1,1],[1,1,2,2],[2,2,3,2]])
##dat_y=np.array([[0,1,1,0],[0,1,1,0],[0,1,1,0]])
###
#filename='R:\B21159\Cali\BMTWBM_COMP_DEC12_JAN13_waves.nc'
#fid=Dataset(filename,'r')
#nd_x=fid.variables['node_X'][:]
#nd_y=fid.variables['node_Y'][:]
#xy=np.transpose(np.vstack((nd_x,nd_y)))
#face=fid.variables['cell_node'][:]
#logi=face[:,3]==0
#face[logi,3]=face[logi,0]
#dat_x=xy[face-1,0]
#dat_y=xy[face-1,1]
#
#px=np.linspace(np.min(dat_x[:]),np.mean(dat_x[:]),num=20)
#py=np.linspace(np.mean(dat_y[:]),np.max(dat_y[:]),num=20)
#pts=np.meshgrid(px,py)
#px=np.reshape(pts[0],np.size(pts[0]),1)
#py=np.reshape(pts[1],np.size(pts[1]),1)
#
##
###px=np.array([px[97]])
###py=np.array([py[97]])
##
###tic=time.clock()
###thiso=np.array([])
###for aa in range (100):
###    px1=np.array([px[aa]])
###    py1=np.array([py[aa]])
###    this=inpoly_py(px1,py1,dat_x,dat_y)
###    thiso=np.append(thiso,this)
###    
###toc=time.clock()
###t_new=toc-tic
###print t_new
###
###tic=time.clock()
###
###thato=np.empty(100)
###thato[:]=np.nan
###for aa in range (100):
###    px1=np.array([px[aa]])
###    py1=np.array([py[aa]])
###    that=inpoly_old(px1,py1,dat_x,dat_y)
###    thato[aa]=that[~np.isnan(that)]
###    thato=np.append(thato,that)
###toc=time.clock()
###t_old=toc-tic
###print t_old
##
#
#
#
#for aa in range (1):
#    px=np.linspace(np.min(dat_x[:]),np.mean(dat_x[:]),num=20)
#    py=np.linspace(np.mean(dat_y[:]),np.max(dat_y[:]),num=20)
#    res_new=inpoly_py(px,py,dat_x,dat_y)
#    px=np.linspace(np.mean([np.min(dat_x[:]),np.mean(dat_x[:])]),np.mean(dat_x[:]),num=20)
#    py=np.linspace(np.mean(dat_y[:]),np.max(dat_y[:]),num=20)
#    tic=time.clock()
#    res_new1=inpoly_py(px,py,dat_x,dat_y)
#    
#toc=time.clock()
#t_new=toc-tic
#print t_new
#
#tic=time.clock()
#
#
#for aa in range (1):
#    res_old=inpoly_old(px,py,dat_x,dat_y)
#toc=time.clock()
#t_old=toc-tic
#print t_old
#
##
