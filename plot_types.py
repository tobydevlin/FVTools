# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 15:35:00 2015

@author: toby.devlin && steven.ettema
"""

import dataset_types
import fvobj as fobj
import numpy as np
import matplotlib.pyplot as plt
import inpoly_py as ip

plt.ion()


class render2D:

    timestep = 0
    interp = 0
    edgecolor = 'none'
    facecolor = 'flat'
    patches = []
    veccolor = 'black'
    vecscale = 1
    vecgrid = 10
    arrows = []

    def settime(self, timestep):
        # Set the timestep and call update
        self.resobj.settime(timestep)
        self.contours.update_patches()

    def setcolormap(self, cdata):
        # Change the colormap of contours... (should this be elsewhere?)
        self.patches.set_array(cdata)

    #---------Patches--------
    def build_patches(self):
        # Start up and generate patch objects
        vertices = self.resobj.get_vertices()
        faces = self.resobj.get_faces()
        self.patches = fobj.mypatches(vertices, faces, self.ax)

        # TODO: Find a better place for this stuff. -- remove MPL from this module
        self.ax.set_xlim((np.min(vertices[0, :])), (np.max(vertices[0, :])))
        self.ax.set_ylim((np.min(vertices[1, :])), (np.max(vertices[1, :])))
        self.c_bar = plt.colorbar(self.patches.patches, ticks=[-1, -0.5, 0, 0.5, 1], ax=self.ax)
        self.c_bar.set_clim(0, 10)
        self.c_bar.draw_all()

    def update_patches(self):
        # Update patch data to new timestep
        t = np.ma.masked_where(np.isnan(self.resobj.var), self.resobj.var)
        self.patches.set_face_value(t)

    def hide_patches(self):
        # Make Patches invisible and not update
        pass

    def destroy_patches(self):
        # Delete patches and cleanup
        pass

    #---------Vectors--------          # TODO: Tidy this up and put some in myarrows. No MPL in this module
    def build_arrows(self):
        #distance between vectors in pixles
        yp1 = self.ax.get_ylim()
        xp1 = self.ax.get_xlim()
        #gets the figure size in pixles
        bbox = self.ax.get_window_extent(). transformed(self.fvobj. fig.dpi_scale_trans.inverted())
        width, height = bbox.width, bbox.height
        width *= self.fvobj.fig.dpi
        height *= self.fvobj.fig.dpi
        #determine the number of vectors in each dimention
        nx = np.round(width / self.vscale)
        ny = np.round(height / self.vscale)
        #detemine there location
        px = np.linspace(xp1[0], xp1[1], nx)
        py = np.linspace(yp1[0], yp1[1], ny)
        #points to plot the arrows on
        pts = np.meshgrid(px, py)
        px = np.reshape(pts[0], np.size(pts[0]), 1)
        py = np.reshape(pts[1], np.size(pts[1]), 1)
        #cell information
        vertices = self.resobj.get_vertices()
        self.face = self.resobj.get_faces() - 1
        xy = vertices
        self.xy = np.transpose(xy)
        x_var, y_var = self.resobj.get_vect_variable(self.vector_xvar, self.vector_yvar)
        self.vectors = fobj.myarrows(x_var, y_var, px, py, self.xy, self.face, self.ax)
        plt.show()

    def hide_arrows(self):
        # Make arrows invisible and not update
        pass

    def destroy_arrows(self):
        # Delete arrows
        pass

    def update_arrows(self):
        #gets the figure size in pixles
        yp1 = self.ax.get_ylim()
        xp1 = self.ax.get_xlim()
        bbox = self.ax.get_window_extent().transformed(self.fvobj.fig.dpi_scale_trans.inverted())
        width, height = bbox.width, bbox.height
        width *= self.fvobj.fig.dpi
        height *= self.fvobj.fig.dpi
        #determine the number of vectors in each dimention
        nx = np.round(width / self.vscale)
        ny = np.round(height / self.vscale)
        #detemine there location
        px = np.linspace(xp1[0], xp1[1], nx)
        py = np.linspace(yp1[0], yp1[1], ny)
        pts = np.meshgrid(px, py)
        px = np.reshape(pts[0], np.size(pts[0]), 1)
        py = np.reshape(pts[1], np.size(pts[1]), 1)
        dat_x = self.xy[self.face, 0]
        dat_y = self.xy[self.face, 1]
        self.datv = ip.inpoly_py(px, py, dat_x, dat_y)
        datx = np.empty(len(self.datv))
        datx[:] = 0
        daty = np.empty(len(self.datv))
        daty[:] = 0
        ind = self.datv != -1
        tmp = self.datv[ind]
        x_var, y_var = self.resobj.get_vect_variable(self.vector_xvar, self.vector_yvar)
        datx[ind] = x_var[tmp.astype(int)]
        daty[ind] = y_var[tmp.astype(int)]

        self.vectors.vectors.set_offsets(np.transpose(np.row_stack((px, py))))
        self.vectors.vectors.set_UVC(datx, daty)
        self.vectors.vectors.X = px
        self.vectors.vectors.Y = py
        self.vectors.vectors.U = datx
        self.vectors.vectors.V = daty
        plt.draw()

    #-------Refresh---------
    def refresh_plot(self, *args):     # The second argument assigns the time step number if you wish
        if len(args) > 0:
            # checks if a float or integer is given, if float it assumes its a time not timestep
            if isinstance(args[0], int):
                self.resobj.timestep = args[0]
            else:
                self.resobj.timestep = np.argmin(abs(self.resobj.time_series - args[0]))
            self.resobj.process_data()
        if self.contours:
            render2D.update_patches(self)
        if self.vectors:
            render2D.update_arrows(self)
        plt.draw()


####__________________________________________________________
class plot_sheet(render2D):

    def __init__(self, fvobj, ax, dfile, variable,
                    ref='sigma', lower=0, upper=1, contours=True, vectors=True, vector_var='V'):

        # take input requests, determine what type of file, then call
        # constructors for the contours and/or vectors
        self.resobj = dataset_types.sheet.factory(dfile, variable, ref, lower, upper)
        self.resobj.timestep = 0
        self.fvobj = fvobj
        self.ax = ax
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
        self.get_t_limits()  # i do this tooextract the res timeonce
        self.add_res_obj()

    def add_res_obj(self):
        # Should this be in the initialisation
        self.fvobj.add_res(self)

    def setref(self, val):
        # Set the reference for depth-averaging
        self.resobj.setref(val)

    def setrange(self, lower, upper):
        # Set the range for depth-averaging
        self.resobj.setrange(lower, upper)
        
    def getref(self):
        # Return the reference for depth-averaging
        pass

    def getrange(self):
        # Return the limits for depth-averaging
        pass

    def get_t_limits(self):
        # Get the start time, end time, and timestep. This will be passed into the slider
        t = self.resobj.get_whole_variable('ResTime')
        self.resobj.time_series = t
        time_bnd = {'time_start': t[0], 'time_end': t[-1], 'time_step': (t[-1]-t[0])/len(t)}
        return time_bnd


#__________________________________________________________
class plot_curtain(render2D):           # TODO: write up a curtain plotting methodology

    def __init__(self, dfile, variable, pline='', chainage=False):
        pass