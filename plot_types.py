# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 15:35:00 2015

@author: toby.devlin && steven.ettema
"""
import dataset_types
import numpy as np
import matplotlib
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
import inpoly_py as ip


class mypatches:
    def __init__(self,vertices,faces,ax):
        patches = []
        for aa in range (0,len(faces)):
            ii = faces[aa,:]
            xy = np.vstack((vertices[0,ii-1],vertices[1,ii-1]))
            polygon = Polygon(np.transpose(xy), True)
            patches.append(polygon)
                
        patches = PatchCollection(patches, cmap=matplotlib.cm.jet,edgecolor ='none')#, alpha=0.4)
        patches.set_array(np.zeros(len(faces)))
        ax.add_collection(patches)
        self.patches=patches

    def delete(self):
        pass
    
    def hide(self):
        pass
    
    def update(self,vertices,faces,ax):
        pass
    
    def set_face_value(self,cdat):
        pass
    
    def set_vertex_value(self,cdat):
        pass

class myarrows:
    def __init__(self,x_var,y_var,px,py,xy,face,ax):
        plt.sca(ax)        
        datv= np.empty((len(px)))
        dat_x=xy[face,0]
        dat_y=xy[face,1]
        datv=ip.inpoly_py(px,py,dat_x,dat_y)
        datx=np.empty((len(datv)))
        datx[:] = np.NAN
        daty=np.empty((len(datv)))
        daty[:] = np.NAN
        ind=~np.isnan(datv)
        tmp=datv[ind]
        datx[ind]=x_var[tmp.astype(int)]
        daty[ind]=y_var[tmp.astype(int)]
        self.vectors = plt.quiver(px,py,datx,daty,units='dots',scale=0.05,minlength=0.01,pivot = 'tail',width=1.5,axes=ax)

class render2D:
    
    timestep=0  
    
    interp=0
    edgecolor='none'
    facecolor='flat'
    patches=[] # collection of polys
    
    veccolor='black'
    vecscale=1
    vecgrid=10
    arrows=[] # quiver
    
    def settime(self,timestep):
        self.resobj.settime(timestep)
        self.contours.update_patches()

    def setcolormap(self,cdata):
        self.patches.set_array(cdata)
    
    	#---------Patches--------
    def build_patches(self):
        vertices = self.resobj.get_vertices()
        faces = self.resobj.get_faces()
        self.patches=mypatches(vertices,faces,self.ax)
        self.ax.set_xlim((np.min(vertices[0,:])),(np.max(vertices[0,:])))
        self.ax.set_ylim((np.min(vertices[1,:])),(np.max(vertices[1,:])))
        self.c_bar=plt.colorbar(self.patches.patches,ticks=[-1, -0.5, 0, 0.5, 1],ax=self.ax)
                
        self.c_bar.set_clim(-1,1)
        self.c_bar.draw_all()

        
    def update_patches(self):
        t=np.ma.masked_where(np.isnan(self.resobj.var),self.resobj.var)
        self.patches.patches.set_array(t)

   
    def hide_patches(self):
        pass

    def destroy_patches(self):
        pass

    #---------Vectors--------
    def build_arrows(self):
        #distance between vectors in pixles 
        yp1 = self.ax.get_ylim()
        xp1 = self.ax.get_xlim()
        #gets the figure size in pixles
        bbox=self.ax.get_window_extent().transformed(self.fvobj.fig.dpi_scale_trans.inverted()) 
        width, height = bbox.width, bbox.height
        width *=self.fvobj.fig.dpi
        height *=self.fvobj.fig.dpi
        #determine the number of vectors in each dimention
        nx=np.round(width/self.vscale)
        ny=np.round(height/self.vscale)
        #detemine there location
        px = np.linspace(xp1[0],xp1[1],nx)
        py = np.linspace(yp1[0],yp1[1],ny)
        #points to plot the arrows on
        pts=np.meshgrid(px,py)
        px=np.reshape(pts[0],np.size(pts[0]),1)
        py=np.reshape(pts[1],np.size(pts[1]),1)
        #cell information
        vertices = self.resobj.get_vertices()
        self.face = self.resobj.get_faces()-1
        xy = vertices
        self.xy = np.transpose(xy);
        x_var, y_var=self.resobj.get_vect_variable(self.vector_xvar,self.vector_yvar)
        self.vectors=myarrows(x_var,y_var,px,py,self.xy,self.face,self.ax)
        plt.show()
        
        
    def hide_arrows(self):
        pass

    def destroy_arrows(self):
        pass

    def update_arrows(self):
        #gets the figure size in pixles
        yp1 = self.ax.get_ylim()
        xp1 = self.ax.get_xlim()
        bbox=self.ax.get_window_extent().transformed(self.fvobj.fig.dpi_scale_trans.inverted()) 
        width, height = bbox.width, bbox.height
        width *=self.fvobj.fig.dpi
        height *=self.fvobj.fig.dpi
        #determine the number of vectors in each dimention
        nx=np.round(width/self.vscale)
        ny=np.round(height/self.vscale)
        #detemine there location
        px = np.linspace(xp1[0],xp1[1],nx)
        py = np.linspace(yp1[0],yp1[1],ny)
        pts=np.meshgrid(px,py)
        px=np.reshape(pts[0],np.size(pts[0]),1)
        py=np.reshape(pts[1],np.size(pts[1]),1)
        dat_x=self.xy[self.face,0]
        dat_y=self.xy[self.face,1]
        self.datv=ip.inpoly_py(px,py,dat_x,dat_y)
        datx=np.empty(len(self.datv))
        datx[:] = 0
        daty=np.empty(len(self.datv))
        daty[:] = 0
        ind=self.datv!=-1
        tmp=self.datv[ind]
        x_var, y_var=self.resobj.get_vect_variable(self.vector_xvar,self.vector_yvar)
        datx[ind]=x_var[tmp.astype(int)]
        daty[ind]=y_var[tmp.astype(int)]
        
        self.vectors.vectors.set_offsets(np.transpose(np.row_stack((px,py))))
        self.vectors.vectors.set_UVC(datx,daty)
        self.vectors.vectors.X=px
        self.vectors.vectors.Y=py
        self.vectors.vectors.U=datx
        self.vectors.vectors.V=daty
        plt.draw()
        
    #-------Refresh---------
    def refresh_plot(self,*args): #the second argument assigns the time step number if you wish
        if len(args)>0:
            if isinstance(args[0], int): #checks if a float or integer is given, if float it assumes its a time not timestep
                self.resobj.timestep=args[0]
            else:
                self.resobj.timestep=np.argmin(abs(self.resobj.time_series-args[0]))
            self.resobj.process_data()
        if self.contours:
            render2D.update_patches(self)
        if self.vectors:
            render2D.update_arrows(self)
        plt.draw()
        
        
####__________________________________________________________
class plot_sheet(render2D):

    def __init__(self,fvobj,ax,dfile,variable,ref='sigma',lower=0,upper=1,contours=True,vectors=True,vector_var='V'):
        # take input requests, determine what type of file, then call
        # constructors for the contours and/or vectors
        self.resobj = dataset_types.sheet.factory(dfile,variable,ref,lower,upper)
        self.resobj.timestep = 0
        self.fvobj=fvobj
        self.ax=ax
        self.contours = contours
        self.vectors = vectors
        self.vscale = 20
        self.vector_xvar = vector_var + '_x'
        self.vector_yvar = vector_var + '_y'
        
        if contours:
            self.build_patches()
        if vectors:
        	self.build_arrows()

        self.refresh_plot(0)
        self.get_t_limits() # i do this tooextract the res timeonce
        self.add_res_obj()


        #self.patches.set_face_value(self.resobj.var)        
        #self.patches.patches.colorbar.set_clim(-1,1)  
#<<<<<<< HEAD
    def add_res_obj(self):
            self.fvobj.add_res(self)

#=======
        #res=self

        #self.slider_bar=slider.slider_bar(res)
        
#>>>>>>> refs/remotes/origin/TD
    def setref(self,val):
        self.resobj.setref(val)
        # then update?
        
    def setrange(self,lower,upper):
        self.resobj.setrange(lower,upper)
        # then update?        
        
    def getref(self):
        pass
    
    def getrange(self):
        pass
    
    def get_t_limits(self):
        t=self.resobj.get_whole_variable('ResTime')
        self.resobj.time_series=t;
        time={'time_start':t[0],
        'time_end':t[-1],
        'time_step':(t[-1]-t[0])/len(t)}
        
        return time



#__________________________________________________________
class plot_curtain(render2D):
    
    def __init__(self,dfile,variable,pline='',chainage=False):
        pass

