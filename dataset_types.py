# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 13:38:50 2015

@author: toby.devlin
"""
import dave_c
import file_types
import numpy as np

#__________________________________________________________
def isfvnc(filetype):
    try:
        filetype.fid.Type=='Cell-centred TUFLOWFV output'
        return True
    except Exception:
        return False


#__________________________________________________________        
class dataset:
    
    variable_list='' # private... list of total raw variables to extract
    variable = ''    # expression effectively, possible a list (allows for vectors)
    timestep = 0
    fils = ''       # ultimately a list of files
    var = ''
    
    def parse_expression(self):
        # determine syntax and variables of expression
        # might be able to be defined in this superclass
        pass
    
    def update_timestep(self):
        # move to new timestep and do all processing required to extract data
        # 
        pass
    
    def process_data(self):
        # make data into desired format, either a curtain or a depth averaged 
        # sheet, etc.
        pass
    
    def settime(self,val):
        self.timestep = val
        self.process_data()
        
    def setvar(self,val):
        self.variable = val
        
    
#__________________________________________________________
class sheet(dataset):
    # sheet class. process data involves depth averaging for 3D data
    # can set depth averaging settings.

    ref = ''
    range=''
    
    def factory(dfile,variable,ref,lower,upper):
        filobj=file_types.file_type.open(dfile)
        if filobj.Type==1:
            if isfvnc(filobj):
                return fvsheet(filobj,variable,ref,lower,upper)
            else:
                return 0  # check if gridded, make grid nc
                
        elif filobj.Type==2:
            return 0      # dat file.. dont have this yet.
            
        elif filobj.Type==3:
            return 0        # xmdf.. dont have this yet
            
        else:
            return 0        # throw error in future?
    factory = staticmethod(factory)
    
    def setref(self,ref):
        if ref=='sigma':
            self.ref=1
        elif ref=='depth':
            self.ref=2
        elif ref=='height':
            self.ref=3
        elif ref=='elevation':
            self.ref=4
        elif ref=='top':
            self.ref=5
        elif ref=='bot':
            self.ref=6
        else:
            print 'ERROR: Invlaid Ref Value'
    
    def setrange(self,lower,upper):
        self.lower = lower
        self.upper = upper


#__________________________________________________________            
class fvsheet(sheet):
    # special case of a sheet, uses the different zfaces in different timesteps
    # and between cells
    # depth average to either cell centre or nodes...
    def __init__(self,fil,variable,ref,lower,upper):
        self.variable = variable
        
        if isinstance(fil, basestring):
            self.fils = file_types.nc_fil(fil)
        elif isinstance(fil, file_types.file_type):
            self.fils = fil
        
        if self.is3D:
            self.setrange(lower,upper)
            self.setref(ref)
        

                
                
    
    def process_data(self):
        # depth average using fv style
        var = self.get_variable()
        stat = self.fils.get_timestep('stat',self.timestep)
        if self.is3D:
            zl = self.fils.get_timestep('layerface_Z',self.timestep)
            nl = self.fils.get_var('NL')
            idx3 = self.fils.get_var('idx3')
            self.var = dave_c.depth_average(var,zl,nl,idx3,self.ref,self.lower,self.upper)
        else:
            self.var = var
        stat=stat==0 
        self.var[stat] = np.nan
        self.stat=stat
        
    def get_variable(self):
        # Extend this function to handle expressions if required
        var = self.fils.get_timestep(self.variable,self.timestep)
        return var
    
    def get_vect_variable(self,vector_xvar,vector_yvar):
        # Extend this function to handle expressions if required
        x_var = self.fils.get_timestep(vector_xvar,self.timestep)
        y_var = self.fils.get_timestep(vector_yvar,self.timestep)
        return (x_var, y_var)
        
    def is3D(self):
        # Checks once if output will be 3D or not, then stores this
        var = self.get_variable()
        nc3 = self.fils.get_dim_len('NumCells3D')
        nc2 = self.fils.get_dim_len('NumCells2D')
        if len(var)==nc2:
            self.is3D=False
        elif len(var)==nc3:
            self.is3D=True
        else:
            pass # throw error here    
            
        return self.is3D

    def get_vertices(self):
        x=self.fils.get_var('node_X')
        y=self.fils.get_var('node_Y')
        return np.vstack((x,y))

    def get_faces(self):
        face=self.fils.get_var('cell_node')
        logi=face[:,3]==0
        face[logi,3]=face[logi,0]
        return face
    
    def parse_expression(variable):
        pass
    












#__________________________________________________________
class curtain(dataset):
    # special kind of dataset with a pline
    # knows to extract its data along pline for either normal plotting or against chainage
    pline = ''
    spherical='?'


#__________________________________________________________    
class fvcurtain(curtain):
    # special case of curtain which knows how to deal with fv data format
    pass


#__________________________________________________________   