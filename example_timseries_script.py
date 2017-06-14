# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 12:11:52 2016

@author: Steven.Ettema
"""

# example script for a plot of fv timeseries data


import timeseries as ts
import fv_timeseries_plots as fvp
import numpy as np
import matplotlib.dates as mdates


### how to create a profiles file
in_fil='\\\\blaydos\\scratch2\\B22129\\output\\Brunei_001_warmup.nc'
out_fil='\\\\blaydos\\scratch2\\B22129\\output\\Brunei_001_warmup_SE_test_profiles.nc'
c_ids = ts.get_cell_ids(in_fil,[115.07218,115.07018],[5.157194,5.158294])
c_ids =np.array(c_ids)

''' uncomment the below line to recreate the profiles file'''
#ts.create_profile_files(in_fil,out_fil,c_ids)


### how to plot that profiles file


x,V_y=ts.dave_profiles(out_fil,[('V_y')],'CELL_'+str(c_ids[0]),ref='sigma',lower=0,upper=1)
x,V_x=ts.dave_profiles(out_fil,[('V_x')],'CELL_'+str(c_ids[0]),ref='sigma',lower=0,upper=1)
x=ts.convtime(x)
y=np.hypot(V_x,V_y)

# now you have your data to plot


f = fvp.report_figure(n_fig_pp=1)
ax = fvp.report_axes(f,nr=3,nc=1)

fvp.report_plot(ax[0],x,y,tag='Model')
fvp.report_plot(ax[0],x,V_x,tag='Data1')
fvp.report_plot(ax[1],x,y,tag='Model')
fvp.report_plot(ax[1],x,V_y,tag='Data')
fvp.report_plot(ax[2],x,V_x,tag='Data1')
fvp.report_plot(ax[2],x,V_x,tag='Data')

for i in range(3):
    ax[i].grid('on')
    ax[i].format_xdata=mdates.DateFormatter('%YY/%mm/%dd %hh:%mm:%ss')

# good to call after a zoom to fit the dates    
#f.autofmt_xdate()    
    

