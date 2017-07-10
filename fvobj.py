# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 12:47:22 2015
Creates a matplotlib figue and control object
this is done to allow multiple fv sheets to listen out for the same event.

This initiates a slider as well as foward and backward buttons to negotiate the
timeseries

currently takes a logical for weather or not you wish for an axis to be returned
in future will have figure sizing options

returns a handel to the figure and axis

@author: Steven.Ettema
"""
import matplotlib.pyplot as plt
from  matplotlib.widgets import Slider, Button
from matplotlib import dates
import  numpy as np
import convtime

class fvobj:

    def __init__(self,**kwargs):
        #initialises sheets and axes
        self.res_count=0 # number of res obj connected to slider
        self.nr=kwargs.get('nr',0)
        self.nc=kwargs.get('nc',0)
        self.res_fils=[]
        self.time_start=0
        self.time_end=0
        self.time_step=0
        self.time_current=0
        self.ax=[]
        
        if not(any([self.nc==0,self.nr==0])):
            self.fig=plt.figure()            
            for aa in range (self.nr*self.nc):
                tmp=plt.subplot(self.nr, self.nc, aa+1)                
                self.ax.append(tmp)
            ## Creating this here along side all other axes
            axcolor='grey'
            self.ax_slider=plt.axes([0.35, 0.01, 0.3, 0.03], axisbg=axcolor)
            self.ax_fwd=plt.axes([0.1, 0.01, 0.1, 0.04], axisbg=axcolor)
            self.ax_bwd=plt.axes([0.00, 0.01, 0.1, 0.04], axisbg=axcolor)
            self.slider_obj=self.make_slider_obj()
            print 'potato'            

    def make_slider_obj(self,t_start=0,t_end=100,t_current=0,t_step=1): #takes resobj from make plots to initialise slider

        axcolor='grey'
        self.slider = Slider(self.ax_slider, 'Timestep', t_start, t_end, valinit=t_current, slidermax=None, slidermin=None)
        self.fwd = Button(self.ax_fwd,'>>',color=axcolor,hovercolor='0.975')
        self.bwd = Button(self.ax_bwd,'<<',color=axcolor,hovercolor='0.975')
        self.slider.valtext.set_text(convtime.convtime(t_current).isoformat())
       
        def update(val):#link this to the update in each resobj
            t = np.floor(self.slider.val)            
            self.time_current=t
            for aa in range(0,len(self.res_fils)):
                self.res_fils[aa].refresh_plot(self.time_current)
            self.slider.valtext.set_text(convtime.convtime(t).isoformat())
            
        self.slider.on_changed(update)
        
        def go_forwards(event):
            t=self.slider.val
            self.slider.set_val(t+t_step)# this should fire off the update event
        
        self.fwd.on_clicked(go_forwards)
        
        def go_backwards(event):
            t=self.slider.val
            self.slider.set_val(t-t_step)# this should fire off the update event
        
        self.bwd.on_clicked(go_backwards)
        
        
        
        def on_key(event):
            if event.key == 'right':
                t=self.slider.val
                self.slider.set_val(t+t_step)
            elif event.key == 'left':
                t=self.slider.val
                self.slider.set_val(t-t_step)
            elif event.key == 'up':
                t=self.slider.val
                self.slider.set_val(t+t_step*5)
            elif event.key == 'down':
                t=self.slider.val
                self.slider.set_val(t-t_step*5)
            
        if hasattr(self,'cid')==False:
            self.cid = self.fig.canvas.mpl_connect('key_release_event', on_key)
        
        
    def add_res(self,fvplot):
        self.ax_slider.clear()
        self.res_fils.append(fvplot)
        if self.res_count==0:
            time=fvplot.get_t_limits()
            self.time_start=time['time_start']
            self.time_end=time['time_end']
            self.time_step=time['time_step']
            self.res_count==self.res_count+1;
            self.time_current=self.time_start
        else:
            time=fvplot.get_t_limits()
            self.time_start=min(self.time.start,time['time_start'])
            self.time_end=max(self.time.end,time['time_end'])
            self.time_step=min(self.time.step,time['time_step'])
            self.res_count==self.res_count+1;
            
        
        self.make_slider_obj(self.time_start,self.time_end,self.time_current,self.time_step)
                
                #valmax=res.resobj.
                #valmin=
                #time_current=valmin
                #self.make_sl
        pass        
        
        
    def remove_res_obj(self,res):
         pass
        
    def close_res(self):
        plt.close(self.fig)
#t=fvobj(nr=3,nc=2)
        
        
        
        
        
                
        
    
    
