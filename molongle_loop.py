#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 15:24:18 2016

@author: Steven.Ettema
"""

from netCDF4 import Dataset
import csv_tools
import sys
import numpy as np

#modfil = r"\\blaydos\scratch3\B22131\output\MOL_DESI_OPTION_1_004.nc"
#csvfil = r"L:\B22131.L.mpb_Molongle\Modelling\TUFLOWFV\geo\cell_centers\MOLONGLE_003_option_4.csv"

def new_bathy(modfil,csvfil):
    cids=np.array([7918,8064,8200,8334,8461,8586,8704,8825,8935,9044,9152,9260,9365,9464,9559,9642,9722,9797,9859,9925,9985,10043,10095,10097,10136,10138,10139,10134,10091,10037,9977,9916,9852,9789,9708,9623,9539,9443,9343,9235,9129,9023,8911,8802,8684,8568,8437])
    cids=cids-1
    density = 800
    ncdata = Dataset(modfil,'r')
    zb = ncdata.variables['cell_Zb'][:]
    bed_mass_start = ncdata.variables['BED_MASS'][0,:,:]    
    bed_mass_end = ncdata.variables['BED_MASS'][-1,:,:]
    bed_mass_start = np.sum(bed_mass_start,1)
    bed_mass_end = np.sum(bed_mass_end,1)
    bed_mass_diff = bed_mass_end-bed_mass_start
    bed_mass_diff[bed_mass_diff<0]=0
    dzb=bed_mass_diff/density
    z_new=zb
    z_new[cids]=zb[cids]+dzb[cids]
    # sort out the name and write the file
    [date,data,texts,headers] = csv_tools.csv_read(csvfil,'ffff',nheaderlines=1)
    data[3,:]=z_new
    name = csvfil.replace(".csv","_interp.csv")
    with open(name,'wb') as csvfil:
        csvfil.write(','.join(headers)+'\r\n')
        np.savetxt(csvfil,np.transpose(data),fmt='%f',delimiter=',',newline='\r\n')
    #with open(name,'wb') as csvfil:
        #rowwrite = csv.writer(csvfil,delimiter=',')
        #rowwrite.writerow(data[3][:])
        #for line in range(len(z_new)):
                #rowwrite.writerow([data[1][0,line],data[1][1,line],data[1][2,line],z_new[line]])
    return z_new
    

if __name__=="__main__":
    if len(sys.argv) != 3:
        print('Function requires 2 arguments. 1st the result file, then the csv file of the new bathy')
        sys.exit(1)
    modfil = sys.argv[1]
    csvfil = sys.argv[2]
    new_bathy(modfil,csvfil)

        