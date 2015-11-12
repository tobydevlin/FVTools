# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 14:53:54 2015

@author: Steven.Ettema
"""

#make_sheet
import plot_types as pt
import matplotlib.pyplot as plt


fig, ax1 = plt.subplots()

fvobj=pt.plot_sheet('R:\B21159\Cali\BMTWBM_COMP_DEC12_JAN13_waves.nc','H',ref='sigma',lower=0,upper=1,fig=fig,ax=ax1,contours=True,vector_var='V')


#import file_types as ft
#
#t=ft.nc_fil('R:\B21159\Cali\BMTWBM_COMP_DEC12_JAN13_waves.nc')
