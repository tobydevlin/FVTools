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

import matplotlib
import matplotlib.pyplot as plt
from  matplotlib.widgets import Slider, Button
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib import dates
import  numpy as np
import convtime

class mypatches:
    def __init__(self, vertices, faces, ax):
        patches = []
        for aa in range(0, len(faces)):
            ii = faces[aa, :]
            xy = np.vstack((vertices[0, ii - 1], vertices[1, ii - 1]))
            polygon = Polygon(np.transpose(xy), True)
            patches.append(polygon)

        patches = PatchCollection(patches, cmap=matplotlib.cm.jet, edgecolor='none')
        patches.set_array(np.zeros(len(faces)))
        ax.add_collection(patches)
        self.patches = patches

    def delete(self):
        pass

    def hide(self):
        pass

    def update(self, vertices, faces, ax):
        pass

    def set_face_value(self, cdat):
        # Update face centered Data
        self.patches.set_array(cdat)

    def set_vertex_value(self, cdat):
        pass


class myarrows:
    def __init__(self, x_var, y_var, px, py, xy, face, ax):
        plt.sca(ax)
        datv = np.empty((len(px)))
        dat_x = xy[face, 0]
        dat_y = xy[face, 1]
        datv = ip.inpoly_py(px, py, dat_x, dat_y)
        datx = np.empty((len(datv)))
        datx[:] = np.NAN
        daty = np.empty((len(datv)))
        daty[:] = np.NAN
        ind = ~np.isnan(datv)
        tmp = datv[ind]
        datx[ind] = x_var[tmp.astype(int)]
        daty[ind] = y_var[tmp.astype(int)]
        self.vectors = plt.quiver(px, py, datx, daty,
        units='dots', scale=0.05, minlength=0.01, pivot='tail', width=1.5, axes=ax)


class fvobj:
# This 'fvobj' is the figure object that holds a slider and can have resobjs added to it.
# TODO: add capacity to have multiple axes somehow

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
            self.ax_slider=plt.axes([0.35, 0.01, 0.3, 0.03], facecolor=axcolor)
            self.ax_fwd=plt.axes([0.1, 0.01, 0.1, 0.04], facecolor=axcolor)
            self.ax_bwd=plt.axes([0.00, 0.01, 0.1, 0.04], facecolor=axcolor)
            self.slider_obj=self.make_slider_obj()

    def make_slider_obj(self,t_start=0,t_end=100,t_current=0,t_step=1): # TODO: this needs to be put in a separate object

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
        # Add object to plot
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
        # Get rid of results dataset object
        pass
        
    def close_res(self):
        # Close and Cleanup
        plt.close(self.fig)      


class sliderobj:
    # Slider object with start time, end time, small step and large step.
    # Needs to return the timestep it is at when clicked.
    # Should also allow extending the times when a new object is added
    pass
