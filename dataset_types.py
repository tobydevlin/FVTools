# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 13:38:50 2015

@author: toby.devlin
"""
import file_types
import numpy as np
import Util_Engine

#__________________________________________________________
def isfvnc(filetype):
    try:
        filetype.fid.Type == 'Cell-centred TUFLOWFV output'
        return True
    except Exception:
        return False


#__________________________________________________________
class dataset:

    variable_list = ''  # private... list of total raw variables to extract
    variable = ''    # expression effectively, possible a list (allows for vectors)
    timestep = 0
    fils = ''       # ultimately a list of files
    var = ''

    def parse_expression(self):
        # determine syntax and variables of expression
        # might be able to be defined in this superclass
        import re
        expr = self.var
        subvars = [a.upper() for a in re.split('[\W0-9]+', expr)]
        vars = nci.variables
        # find which variables have time dimension
        for aa in range(len(subvars)):
            if subvars[aa] not in vars:
                print('Error')
            else:
                expr = re.sub(subvars[aa], 'nci.variables["' + subvars[aa] + '"][#][:]', expr)

        #eval(('nci.variables["'+var1+'"][1][:]+nci.variables["'+var2+'"][1][:]'))

    def update_timestep(self):
        # move to new timestep and do all processing required to extract data
        #
        pass

    def process_data(self):
        # make data into desired format, either a curtain or a depth averaged
        # sheet, etc.
        pass

    def settime(self, val):
        self.timestep = val
        self.process_data()

    def setvar(self, val):
        # 
        self.variable = val

    def get_variable(self):
        # Extend this function to handle expressions if required - Only reason it is still a thing, it might call multiple variables
        var = self.fils.get_timestep(self.variable, self.timestep)
        return var


#__________________________________________________________
class sheet(dataset):
    # sheet class. process data involves depth averaging for 3D data
    # can set depth averaging settings.


    def factory(dfile, variable, ref, lower, upper):
        filobj = file_types.file_type.open(dfile)
        if filobj.Type == 1:
            if isfvnc(filobj):
                return fvsheet(filobj, variable, ref, lower, upper)
            else:
                return 0  # check if gridded, make grid nc

        elif filobj.Type == 2:
            return 0      # dat file.. dont have this yet.

        elif filobj.Type == 3:
            return 0        # xmdf.. dont have this yet

        else:
            return 0        # throw error in future?
    factory = staticmethod(factory)

    def setref(self, ref):
        # Get Depth averaging function that is appropriate for ref.
        self.ref=Util_Engine.get_dave_fun(ref)

    def get_vect_variable(self, vector_xvar, vector_yvar):
        # Extend this function to handle expressions if required
        x_var = self.fils.get_timestep(vector_xvar, self. timestep)
        y_var = self.fils.get_timestep(vector_yvar, self. timestep)
        return (x_var, y_var)

    def setrange(self, lower, upper):
        # Set upper and lower bound of depth-averaging
        self.lower = lower
        self.upper = upper


#__________________________________________________________
class fvsheet(sheet):
    # special case of a sheet, uses the different zfaces in different timesteps
    # and between cells
    # depth average to either cell centre or nodes...
    def __init__(self, fil, variable, ref, lower, upper):
        self.variable = variable

        if isinstance(fil, str):
            self.fils = file_types.nc_fil(fil)
        elif isinstance(fil, file_types.file_type):
            self.fils = fil

        if self.is3D:
            self.setrange(lower, upper)
            self.setref(ref)

    def process_data(self):
        # depth average using fv style
        var = self.get_variable()
        stat = self.fils.get_timestep('stat', self.timestep)
        if self.is3D:
            zl = self.fils.get_timestep('layerface_Z', self.timestep)
            nl = self.fils.get_var('NL')
            idx3 = self.fils.get_var('idx3')
            nc2=idx3.size
            self.var = np.zeros(nc2,dtype=np.float32)
            err = self.ref(var, zl, nl, idx3, self.lower, self.upper, self.var, idx3.size)
        else:
            self.var = var
        stat = stat == 0
        self.var[stat] = np.nan
        self.stat = stat
        
    def get_variable(self):
        # Extend this function to handle expressions if required
        var = self.fils.get_timestep(self.variable, self.timestep)
        return var

    def get_whole_variable(self, variable):
        var = self.fils.get_var(variable)
        return var

    def get_vect_variable(self, vector_xvar, vector_yvar):
        # Extend this function to handle expressions if required
        x_var = self.fils.get_timestep(vector_xvar, self.timestep)
        y_var = self.fils.get_timestep(vector_yvar, self.timestep)
        return (x_var, y_var)

    def is3D(self):
        # Checks once if output will be 3D or not, then stores this
        var = self.get_variable()
        nc3 = self.fils.get_dim_len('NumCells3D')
        nc2 = self.fils.get_dim_len('NumCells2D')
        if len(var) == nc2:
            is3D = False
        elif len(var) == nc3:
            is3D = True
        else:
            pass  # throw error here
        return is3D

    def get_vertices(self):
        x = self.fils.get_var('node_X')
        y = self.fils.get_var('node_Y')
        return np.vstack((x, y))

    def get_faces(self):
        face = self.fils.get_var('cell_node')
        logi = face[:, 3] == 0
        face[logi, 3] = face[logi, 0]
        return face


#__________________________________________________________
class curtain(dataset):
    # special kind of dataset with a pline
    # knows to extract its data along pline for either normal plotting or against chainage
    pline = ''
    spherical = '?'

    # This is here until i can find a clever way to get this and the sheet version into 'dataset'
    def factory(dfile, variable, pline):
        filobj = file_types.file_type.open(dfile)
        if filobj.Type == 1:
            if isfvnc(filobj):
                return fvcurtain(filobj, variable, pline)
            else:
                return 0  # check if gridded, make grid curtain nc

        elif filobj.Type == 2:
            return 0      # dat file.. can these be curtains?

        elif filobj.Type == 3:
            return 0        # xmdf.. can these be curtains?

        else:
            return 0        # throw error in future?
    factory = staticmethod(factory)


#__________________________________________________________
class fvcurtain(curtain):
    # special case of curtain which knows how to deal with fv data format
    pass


#__________________________________________________________