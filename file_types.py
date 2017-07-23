# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 11:09:22 2015

@author: toby.devlin
"""
from netCDF4 import Dataset


'''
all of this code is meant to be simple io interfaces to different files
anything more complicated, ie. how to get different things out of these in
different formats, needs to be done in the dataset_types
'''

#__________________________________________________________
class file_type:
    # Superclass for different types of results files
    fid='';  # dfile ID
    
    def get_timestep():
        # gets a variable at a particular timestep 
        pass       
    
    def get_var():
        # gets a variable at all timesteps        
        pass
    
    def get_dim_len(name):
        # get length of dimension
        pass
    
    # Other Suggested Methods
    def inq_var():
        # Check if variable exists (and is 3D)
        pass
    
    def get_time():
        # return vector of time
        pass
    
    def open(dfile):
        
        try: # TUFLOWFV netcdf
            ff = Dataset(dfile,'r')
            ff.close()
            return nc_fil(dfile)
        except Exception:
            # place an error if it cant read the ncfile
            pass
        
        try: # xmdf
            # some checks
            pass
        except Exception:
            pass
        
        try: # dat
            # some checks
            pass
        except Exception:
            pass
    open = staticmethod(open)
    
    def close():
        # close file, might be triggered on deletion
        pass


#__________________________________________________________
class nc_fil(file_type):
    # class to specifically interact with netcdf files
    
    def __init__(self,filename):
        self.fid = Dataset(filename,'r')
        self.Type=1
    
    def get_timestep(self,variable,timestep):
        # gets a variable at a particular timestep 
        var=self.fid.variables[variable][timestep]
        return var
    
    def get_var(self,variable):
        # gets a variable at all timesteps        
        return self.fid.variables[variable][:]
        
    def get_dim_len(self,name):
        return len(self.fid.dimensions[name])


#__________________________________________________________
class dat_fil(file_type):
    # class to specifically interact with dat files
    
    def __init__(self,filename):
        self.Type=2
        
    def get_timestep():
        # gets a variable at a particular timestep 
        pass
    
    def get_var():
        # gets a variable at all timesteps        
        pass


#__________________________________________________________
class xmdf_fil(file_type):
    # class to specifically interact with xmdf files
    
    def __init__(self,filename):
        self.Type=3
        
    def get_timestep():
        # gets a variable at a particular timestep 
        pass
    
    def get_var():
        # gets a variable at all timesteps        
        pass
    