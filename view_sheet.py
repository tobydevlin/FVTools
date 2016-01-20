# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 14:53:54 2015

@author: Steven.Ettema
"""

#make_sheet
import plot_types as pt
import fvobj as ctrl


fv_obj=ctrl.fvobj(nr=1,nc=2)

fvobjz0=pt.plot_sheet(fv_obj,fv_obj.ax[0],'R:\B21159\Cali\BMTWBM_COMP_DEC12_JAN13_waves.nc','H',ref='sigma',lower=0,upper=1,contours=True,vectors=True,vector_var='V')
fvobjz1=pt.plot_sheet(fv_obj,fv_obj.ax[1],'R:\B21159\Cali\BMTWBM_COMP_DEC12_JAN13_waves.nc','V_x',ref='sigma',lower=0,upper=1,contours=True,vectors=True,vector_var='V')


fv_obj.ax[0].get_xaxis().set_visible(False)
fv_obj.ax[0].get_yaxis().set_visible(False)
fv_obj.ax[1].get_xaxis().set_visible(False)
fv_obj.ax[1].get_yaxis().set_visible(False)

fv_obj.ax[0].axis('equal')
fv_obj.ax[1].axis('equal')

print 'french fries'

#import file_types as ft
#
#t=ft.nc_fil('R:\B21159\Cali\BMTWBM_COMP_DEC12_JAN13_waves.nc')
#for aa in range(10):
#    t=fv_obj.time_current
#    fv_obj.slider.set_val(t+aa*fv_obj.time_step)
#    
#fv_obj.close_res()