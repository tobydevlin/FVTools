# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 09:48:03 2015

@author: toby.devlin
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 14:31:36 2015

@author: toby.devlin
"""

import numpy as np

def mymin(a, b): return a if a<=b else b
def mymax(a, b): return a if a>=b else b
def mymid(a, b, c):
    if b>=c:
        return c
    elif b<=a:
        return a
    else:
        return b

def depth_average(var3,zl,nl,idx3,ref,lower,upper):
    return engine(var3,zl,nl,idx3,ref,lower,upper)

def engine(var3, zl, nl, idx3, ref, lower, upper):


    nc2=np.size(idx3)
    nc3=np.size(var3)
    var2=np.zeros(nc2, dtype=np.float32)     
    frc=np.zeros(nc3, dtype=np.float32)
    NAN=float("NaN")
        
    for a in range(nc2):
        itop=idx3[a]+a-1        
        ibot=itop+nl[a]
        
        if ref==1:#'sigma':
            d1=(1-lower)*zl[ibot]+lower*zl[itop]
            d2=(1-upper)*zl[ibot]+upper*zl[itop]
        elif ref==2:#'height':
            d1=zl[ibot]+lower
            d2=mymin(zl[itop],zl[ibot]+upper)
        elif ref==3:#'depth':
            d1=mymax(zl[ibot],zl[itop]-upper)
            d2=zl[itop]-lower
        elif ref==4:#'elevation':
            d1=mymax(lower,zl[ibot])
            d2=mymin(upper,zl[itop])
        elif ref==5:#'top':
            id1=mymin(itop+upper,ibot)
            d1=zl[id1]
            d2=zl[itop+lower-1]
        elif ref==6:#'bot':
            d1 = zl[ibot-lower+1]
            id2=mymax(ibot-upper,itop)
            d2 = zl[id2]
        else:
            print 'error in ref name'
            return 1

        d=d2-d1
        if d==0:
            var2[a]=NAN
            for b in range(nl[a]):   
                frc[a+b]=NAN
        else:
            for b in range(nl[a]):
                up=mymid(d1,zl[a+b],d2)
                down=mymid(d1,zl[a+b+1],d2)
                frc[a+b]=(up-down)/d
                var2[a]=var2[a]+(up-down)/d*var3[a+b]
    
    return frc