# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 10:00:22 2015

@author: toby.devlin
"""
import numpy as np
from netCDF4 import Dataset

ncfil=Dataset('B:/Gladstone_corals/GLAD_EXT_CALI_3D_001_dev.nc','r')
timestep=1
variables='V_x'
Ref='elevation'
lower=-11.2
upper=-5.6


def mymin(a,b): return a if a<=b else b
def mymax(a,b): return a if a>=b else b
def mymid(a,b,c):
    if b>=c:
        return c
    elif b<=a:
        return a
    else:
        return b

def sigma_fun(zl,itop,ibot,lower,upper):
    d1=(1-lower)*zl[ibot]+lower*zl[itop]
    d2=(1-upper)*zl[ibot]+upper*zl[itop]
    return d1, d2

def elevation_fun(zl,itop,ibot,lower,upper):
    d1=mymax(lower,zl[ibot])
    d2=mymin(upper,zl[itop])
    return d1, d2

def height_fun(zl,itop,ibot,lower,upper):
    d1=zl[ibot]+lower
    d2=mymin(zl[itop],zl[ibot]+upper)
    return d1, d2

def depth_fun(zl,itop,ibot,lower,upper):
    d1=mymax(zl[ibot],zl[itop]-upper)
    d2=zl[itop]-lower
    return d1, d2

def top_fun(zl,itop,ibot,lower,upper):
    id1=mymin(itop+upper,ibot)
    d1=zl[id1]
    d2=zl[itop+lower-1]
    return d1, d2

def bot_fun(zl,itop,ibot,lower,upper):
    d1 = zl[ibot-lower+1]
    id2=mymax(ibot-upper,itop)
    d2 = zl[id2]
    return d1, d2


def depth_average(var3,zl,nl,idx3,ref,lower,upper):

    
    nc2=np.size(idx3)
    
    if ref=='sigma':
        dfun = sigma_fun
    elif ref=='height':
        dfun = height_fun
    elif ref=='depth':
        dfun ='depth_fun'
    elif ref=='top':
        dfun='top_fun'
    elif ref=='bot':
        dfun=bot_fun
    else:
        print 'error in ref name'
        return 1
    
    
    var2=np.zeros(nc2)
    for a in range(nc2):
        itop=idx3[a]+a-1        
        ibot=itop+nl[a]
        d1, d2=dfun(zl,itop,ibot,lower,upper)

        d=d2-d1
        
        for b in range(nl(a)):
            up=mymid(d1,zl[a+b],d2)
            down=mymid(d1,zl[a+b+1],d2)
            var2[a]=var2[a]+(up-down)/d*var3[a+b]

            
    return var2    
        
var3=ncfil.variables[variables][timestep] #3D variable
zl=ncfil.variables['layerface_Z'][timestep] # zfaces
nl=ncfil.variables['NL']                    # number of layers for each cell
idx3=ncfil.variables['idx3']                #         

    