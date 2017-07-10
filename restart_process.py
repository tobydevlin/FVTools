# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 12:18:27 2016

@author: Steven.Ettema
"""
import numpy as np
import struct

def read_restat(fil,precision):
    f = open(fil,"rb")
    try:
        time = np.fromfile(f,dtype=np.float64,count=1)
        NC2 = np.fromfile(f,dtype=np.int32,count=1)
        NC3 = np.fromfile(f,dtype=np.int32,count=1)
        NU = np.fromfile(f,dtype=np.int32,count=1)
        if precision.lower() == 'single':
            Zb = np.fromfile(f,dtype=np.float32,count=NC2)
            U = np.fromfile(f,dtype=np.float32,count=NU*NC3)
        elif precision.lower() == 'double':
            Zb = np.fromfile(f,dtype=np.float64,count=NC2)
            U = np.fromfile(f,dtype=np.float64,count=NU*NC3)
        
        U=U.reshape([NU,NC3])
    finally:
        f.close()
    return time,NC2,NC3,NU,Zb,U

def write_restart(outfil,t,Zb,U,precision):

# inputs:
#   rstfil = 'name of .rst file to create'
#   t = time in seconds since 01/01/1990
#   Zb = cell elevations
#   U = (NC3,NV) where NV = 3 (depth, V_x*depth, V_y*depth) + all scalars*depth
#   float = 'single' or 'double'

    NC2 = len(Zb)
    NC3 = U.shape[1]
    NU = U.shape[0]
    f = open(outfil,"wb")
    try:
        f.write(struct.pack('d',t))
        f.write(struct.pack('i',NC2))
        f.write(struct.pack('i',NC3))
        f.write(struct.pack('i',NU))
        if precision.lower() =='single':
            tmp=Zb.astype('float32')
            tmp.tofile(f)
            tmp=U.astype('float32')
            for aa in range(tmp.shape[1]):
                for bb in range(tmp.shape[0]):
                    f.write(struct.pack('<f',tmp[bb,aa]))
        elif precision.lower() == 'double':
            tmp=Zb.astype('float64')
            tmp.tofile(f)
            tmp=U.astype('float64')
            for aa in range(tmp.shape[1]):
                for bb in range(tmp.shape[0]):
                    f.write(struct.pack('<d',tmp[bb,aa]))
    finally:
        f.close()

    return


# Testing
# fil = r'L:\B21159.L.iat.MurrayMouthDredging\modelling\TUFLOWFV_3\input\calibration\log\MURRAY_CALI_003.rst'
# [time,NC2,NC3,NU,Zb,U]=read_restat(fil,'single')
#
# outfil = r'L:\B21159.L.iat.MurrayMouthDredging\modelling\TUFLOWFV_3\input\calibration\log\MURRAY_CALI_003_compare.rst'
# write_restart(outfil,time,Zb,U,'single')