#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 10:03:57 2016

@author: Steven.Ettema
"""

from netCDF4 import Dataset
import restart_process
import csv_tools
import sys
import numpy as np

modfil = r"\\blaydos\scratch2\B21159\TUFLOW_FV\output\MURRAY_HIND_001_01012015_03032015.nc"
csvfil = r"L:\B21159.L.iat.MurrayMouthDredging\modelling\TUFLOWFV_3\geo\cell_centers\survey_interps\20150303.csv"


def new_bathy(modfil,csvfil):
    ncdata = Dataset(modfil,'r')
    zb = ncdata.variables['ZB'][-1,:]
    [date,data,texts,headers] = csv_tools.csv_read(csvfil,'ffff',nheaderlines=1)
    z_new=data[3,:]
    z_new[z_new==9999]=zb[z_new==9999]
    data[3,:]=z_new
    data=data.transpose()
# sort out the name and write the file
    name = csvfil.replace(".csv","_interp.csv")
    with open(name,'wb') as csvfil:
        csvfil.write(','.join(headers)+'\r\n')
        np.savetxt(csvfil,data,fmt='%f',delimiter=',',newline='\r\n')
    #with open(name,'wb') as csvfil:
        #rowwrite = csv.writer(csvfil,delimiter=',')
        #rowwrite.writerow(data[3][:])
        #for line in range(len(z_new)):
                #rowwrite.writerow([data[1][0,line],data[1][1,line],data[1][2,line],z_new[line]])
    return z_new
    
def generate_next_rst(modfil,z_new):
    ncdata = Dataset(modfil,'r')
    NC2 = len(ncdata.variables['V_x'][-1])
    H = ncdata.variables['H'][-1]
    rst_out = np.zeros([5,NC2])
    rst_out[0,:]=H-z_new
    rst_out[rst_out<0]=0
    rst_out[1,:]=ncdata.variables['V_x'][-1,:]*rst_out[0,:]
    rst_out[2,:]=ncdata.variables['V_y'][-1,:]*rst_out[0,:]
    rst_out[3,:]=ncdata.variables['SAL'][-1,:]*rst_out[0,:]
    rst_out[4,:]=ncdata.variables['TSS'][-1,:]*rst_out[0,:]
    rst_out[np.isnan(rst_out)]=0
    t=ncdata['ResTime'][-1]*3600
    outfil=modfil.split('\\')
    outfil=outfil[-1]
    outfil=outfil.replace('.nc','_new.rst')
    #outfil='log\\'+outfil
    restart_process.write_restart(outfil,t,z_new,rst_out,'single')
    return
z_new = new_bathy(modfil,csvfil)

if __name__=="__main__":
    if len(sys.argv) != 3:
        print('Function requires 2 arguments. 1st the result file, then the csv file of the new bathy')
        sys.exit(1)
    modfil = sys.argv[1]
    csvfil = sys.argv[2]
    z_new = new_bathy(modfil,csvfil)
    generate_next_rst(modfil,z_new)

        