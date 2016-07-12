# -*- coding: utf-8 -*-
"""
Created on Fri Jul 08 16:18:43 2016

@author: Steven.Ettema
"""

import matplotlib.pyplot as plt
import numpy as np

def report_figure(papersize='a4',orientation='Portrait',n_fig_pp=2):
    papersizes = {
    'a0':[841,1189],
    'a1':[594,841],
    'a2':[420,594],
    'a3':[297,420],
    'a4':[210,297],
    'a5':[148,210],
    'a6':[105,148],
    'a7':[74,105],
    'a8':[52,74]}
    
    dims = papersizes[papersize]
    dims = [dims[0], dims[1]/n_fig_pp]
    if orientation == 'Landscape':
        dims = [dims[1], dims[0]]
    
    dims = [dims[0]*0.0393701,dims[1]*0.0393701] #convert from mm too inches
    
    f=plt.figure(figsize=dims,facecolor='white')
    
    return f

def report_axes(f,nr=1,nc=1):
    ax=[]
    for axis in range (nr*nc):
        if axis == 0:
            tmp=f.add_subplot(nr, nc, axis+1)                
        else:
            tmp=f.add_subplot(nr, nc, axis+1, sharex = ax[0])                
        ax.append(tmp)
                
    return ax
    
def clr(n):
    clrs = np.array([(0.7098, 0.9020,  0.0784),
    (1.0000,    0.4078,         0),
    (0.1020,    0.7412,    0.7882),
    (0.0863,    0.2863,    0.4392),
    (0.6627,    0.0627,    0.0431),
    (0.0431,    0.6588,    0.0627),
    (0.2824,    0.2980,    0.7686),
    (1.0000,    0.9020,         0),
     (0,    0.8706,    1.0000),
    (0.6667,    0.8196,    0.7176),
    (0.7098,    0.8314,    0.3216),
         (0,         0,         0)]) 
    if n>clrs.shape[0]:
        print "No color pallet color exists for "+str(n)+ " please try again"
    
    return clrs[n,:]
    

def report_plot(axis,x,y,tag = 'Model'):
    clrs = {'Model':clr(0),
            'Data':clr(1),
            'Data1':clr(2)}
    lines = {'Model':'-',
            'Data':'None',
            'Data1':'None'}
    alphas = {'Model':1,
            'Data':0.75,
            'Data1':0.75}
            
    axis.plot(x,y,color=clrs[tag],linestyle=lines[tag],marker='.',alpha=alphas[tag])
    
    
