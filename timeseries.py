# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 16:23:06 2016

@author: Steven.Ettema
"""

import numpy as np
from netCDF4 import Dataset
#import matplotlib.pyplot as plt
#import matplotlib.dates as mdates



def get_cell_ids(ncfil,x,y):
    '''   
    get_cell_ids is a useful function that will return the TUFLOW FV cell id 
    for a given x and y location
    
    inputs are :
    --------------------------------------------------------------------------
    the netcdf results file (ncfil)
    the x and y locations of the cells you wish to index - these must be stored 
        as an array i.e x=[133.2], y=[-2.35]
    
    outputs are :
    --------------------------------------------------------------------------
    the 2d cell id for the TUFLOW FV results. Note that when using as an index
    from timeseries these cells must have 1 taken from them (python indexing scheme)
        
    '''
    
    ncfil=Dataset(ncfil,'r')
    node_x=ncfil.variables['node_X'][:]
    node_y=ncfil.variables['node_Y'][:]
    cell_node=ncfil.variables['cell_node'][:]
    cid=[np.nan]*len(x)
    for bb in range (0,len(x)):
        coords=np.vstack((node_x,node_y))
        "inside cell"
        'first find the nearest node'
        # maybe get all the ids here?
        dx=x[bb]-node_x
        dy=y[bb]-node_y
        dis=np.hypot(dx,dy)
        id_c=np.argmin(dis)
        tmp=np.where(cell_node==id_c)
        logi=[False]*len(tmp[0])
        for aa in range (0,len(tmp[0])):
            verts=cell_node[tmp[0][aa]] #converting to zero as the initial value
            if verts[3]==0:
                verts[3]=verts[0]
            poly_x=coords[0,verts]
            poly_y=coords[1,verts]
            poly=np.transpose(np.vstack((poly_x,poly_y)))
            logi[aa]=point_inside_polygon(x[bb],y[bb],poly)
            if logi[aa]==True:
                cid[bb]=tmp[0][aa]
                break
    return cid
        
def point_inside_polygon(x,y,poly):
    '''
    My own inpoly like function because YOLO
    '''
    n = len(poly)
    inside =False
    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y >= min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):#check that the data is in the correct range (to the left)
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x #determines intercept with the segment
                    if p1x == p2x or x <= xinters:
                        inside = not inside
    p1x,p1y = p2x,p2y
    return inside



#function used to get extraction data for 2d - 2d cells
def extract_3D_cells(nc_fid,c_ids):
    '''
    inputs are :
    --------------------------------------------------------------------------
    the open netcdf results file (nc_fid)
    the 2d cell Ids for which you want the 3D cells (c_ids)
    
    outputs are :
    --------------------------------------------------------------------------
    an array of the 3d cell ids (start and end id) - (id_3)
    an array which indexes the first 3D cell of each extracted 2D cell
    
    '''
    id_3=np.zeros([2,len(c_ids)])
    id_3[0,:]=nc_fid.variables['idx3'][c_ids-1]-1 #index from zero
    id_3[1,:]=id_3[0,:]+nc_fid.variables['NL'][c_ids-1]-1
    arr=np.array([])
    for aa in range(id_3.shape[1]):
        arr=np.hstack((arr, np.arange(id_3[0,aa],id_3[1,aa]+1)))
    arr=arr.astype('int32')
    lf_3=np.zeros([2,len(c_ids)])
    lf_3[0,:]=nc_fid.variables['idx3'][c_ids-1]-1+c_ids-1 #index from zero
    lf_3[1,:]=lf_3[0,:]+nc_fid.variables['NL'][c_ids-1]
    arrlf=np.array([])
    for aa in range(lf_3.shape[1]):
        arrlf=np.hstack((arrlf, np.arange(lf_3[0,aa],lf_3[1,aa]+1)))
    arrlf=arrlf.astype('int32')   
    
    return id_3, arr, lf_3, arrlf
    
def ncdump(nc_fid, verb=False):
    '''
    ncdump outputs dimensions, variables and their attribute information.
    The information is similar to that of NCAR's ncdump utility.
    ncdump requires a valid instance of Dataset.

    Parameters
    ----------
    nc_fid : netCDF4.Dataset
        A netCDF4 dateset object
    verb : Boolean
        whether or not nc_attrs, nc_dims, and nc_vars are printed

    Returns
    -------
    nc_attrs : list
        A Python list of the NetCDF file global attributes
    nc_dims : list
        A Python list of the NetCDF file dimensions
    nc_vars : list
        A Python list of the NetCDF file variables
    '''
    def print_ncattr(key):
        """
        Prints the NetCDF file attributes for a given key

        Parameters
        ----------
        key : unicode
            a valid netCDF4.Dataset.variables key
        """
        try:
            print "\t\ttype:", repr(nc_fid.variables[key].dtype)
            for ncattr in nc_fid.variables[key].ncattrs():
                print '\t\t%s:' % ncattr,\
                      repr(nc_fid.variables[key].getncattr(ncattr))
        except KeyError:
            print "\t\tWARNING: %s does not contain variable attributes" % key

    # NetCDF global attributes
    nc_attrs = nc_fid.ncattrs()
    if verb:
        print "NetCDF Global Attributes:"
        for nc_attr in nc_attrs:
            print '\t%s:' % nc_attr, repr(nc_fid.getncattr(nc_attr))
    nc_dims = [dim for dim in nc_fid.dimensions]  # list of nc dimensions
    # Dimension shape information.
    if verb:
        print "NetCDF dimension information:"
        for dim in nc_dims:
            print "\tName:", dim 
            print "\t\tsize:", len(nc_fid.dimensions[dim])
            print_ncattr(dim)
    # Variable information.
    nc_vars = [var for var in nc_fid.variables]  # list of nc variables
    if verb:
        print "NetCDF variable information:"
        for var in nc_vars:
            if var not in nc_dims:
                print '\tName:', var
                print "\t\tdimensions:", nc_fid.variables[var].dimensions
                print "\t\tsize:", nc_fid.variables[var].size
                print_ncattr(var)
    return nc_attrs, nc_dims, nc_vars

    
def create_profile_files_engine(nc,w_nc_fid,c_ids,time_steps):
    '''
    Used to create a netcdf profiles style file
    inputs are :
    --------------------------------------------------------------------------
    nc - the open netcdf file results file which you wish to extract
    w_nc_fid - the open new netcdf file you wish to write the profiles file too
    c_ids - the tuflow_fv 2d cell Id for the profiles file
    time_steps - a array of timesteps you wish to extract from the netcdf file
    
    outputs are: 
    --------------------------------------------------------------------------
    The file
    
    '''
    # get the 3D cell ids
    id_3 ,c_ids3,lf_3, lf_ids3 = extract_3D_cells(nc,c_ids)
    _,_,names=ncdump(nc)
    # remove the variables that we dont want in the profiles file
    rem = ['cell_Nvert','cell_node','NL','idx2','idx3',\
    'cell_A','node_X','node_Y','node_Zb']
    for name in rem: 
        if name in names:
            names.remove(name)
    #get the variables dimentions
    n2dc = nc.dimensions['NumCells2D'].size
    n3dc = nc.dimensions['NumCells3D'].size
    nuc = nc.dimensions['Time'].size
    nlf = nc.dimensions['NumLayerFaces3D'].size
    
           
    # Set up the outfut file
    w_nc_fid.description = "TUFLOW-FV Profiles file processed from the original \
    file %s" %(nc.filepath())
    w_nc_fid.createDimension('N1',size=1)
    w_nc_fid.createDimension('Time',size=0)
    w_nc_fid.createDimension('NumSedFrac',size=1)
    for at in nc.ncattrs():
        w_nc_fid.setncattr(at, str(nc.getncattr(at))) 
    
    
    #loop through the variables
    for name in names:
        print(name,  nc.variables[name].shape)
        # determine if the data is 1D (time) 2D, 3D, 4D (bed mass stuff) or 0D (cell information)
        dims=nc.variables[name].shape
        if (len(dims)==1) & (dims[0]==nuc): order=1
        elif len(dims)==2: 
            if dims[1]==n2dc:
                order=2
            elif ((dims[1]==n3dc)&(n3dc!=n2dc))|(dims[1]==nlf):
                order=3
        else:
            order=0
        
        aa=dims[-1]
        if (aa==n2dc)|(aa==n3dc): subtype=1
        elif aa==nlf: subtype=2
        else: subtype = 0
        
        #next extract the data
        if order == 0:
            var_data = nc.variables[name][c_ids-1]
        if order == 1:
            var_data = nc.variables[name][time_steps]
        elif order == 2:
            var_data = nc.variables[name][time_steps,c_ids-1]
        elif order == 3:
            if subtype==1:
                var_data = nc.variables[name][time_steps,c_ids3]
                #id_out=np.cumsum(np.vstack(([0],np.transpose(np.diff(id_3,axis=0))))) #indexes out the array for the different data points
            elif subtype == 2:
                var_data = nc.variables[name][time_steps,lf_ids3]
                #id_out=np.cumsum(np.vstack(([0],np.transpose(np.diff(lf_3,axis=0))))) 
                #indexes out the array for the different data points
            else:
                print 'Unspecified dimentions probably trying to do bed mass, will get to this when someone discovers this short comming SE 2016'
            
        cnt=0
        ed_rng=0
        for cell in c_ids:
            cell_name = 'CELL_'+str(cell)
            if name==names[0]:
                tmp=w_nc_fid.createGroup(cell_name)
                tmp.createDimension('NumLayers',size=nc.variables['NL'][cell-1])
                tmp.createDimension('NumLayerFaces',size=nc.variables['NL'][cell-1]+1)
            tmp=w_nc_fid.groups.get(cell_name)
            if order == 3:
                if subtype==1:            
                    tmp.createVariable(name,'float32',('Time','NumLayers'),zlib=True,complevel=9)
                    i=-1
                if subtype==2:
                    tmp.createVariable(name,'float32',('Time','NumLayerFaces'),zlib=True,complevel=9)
                    i=0
                st_rng=ed_rng
                ed_rng=int(st_rng+lf_3[1,cnt]-lf_3[0,cnt]+1+i)
                tmp.variables[name][:,:] = var_data[:,range(st_rng,ed_rng)]
                cnt=cnt+1 
            if order == 2:
                tmp.createVariable(name,'float32',('Time'),zlib=True,complevel=9)
                tmp.variables[name][:]=var_data[:,cnt]
                cnt=cnt+1
            if order == 1:
                tmp.createVariable(name,'float32',('Time'),zlib=True,complevel=9)
                tmp.variables[name][:]=var_data[:]
            if order == 0:
                tmp.createVariable(name,'float32',('N1'),zlib=True,complevel=9)
                tmp.variables[name][:]=var_data[cnt]
                cnt=cnt+1
            v=tmp.variables[name]
            for at in nc.variables[name].ncattrs():
                v.setncattr(at, str(nc.variables[name].getncattr(at)))

    
def create_profile_files(in_fil,out_fil,c_ids):
    '''
    Used to create a netcdf profiles style file
    inputs are :
    --------------------------------------------------------------------------
    in_fil - the netcdf file results file which you wish to plot
    out_fil - the new netcdf file you wish to write the profiles file too
    c_ids - the tuflow_fv 2d cell Id for the profiles file
       
    outputs are: 
    --------------------------------------------------------------------------
    nil   
    '''
    # load the data in
    nc = Dataset(in_fil,'r')
    w_nc_fid = Dataset(out_fil,'w',format='NETCDF4')
    nt=nc.variables['ResTime'].shape[0]
    time_steps=np.arange(0,nt)
    try:
        create_profile_files_engine(nc,w_nc_fid,c_ids,time_steps)
    finally:
        nc.close()
        w_nc_fid.close()
        
    
   
def dave_profiles(profile_fil,var,cell_name,ref='sigma',lower=0,upper=1):
    '''
    Should probabily rename to dave profiles or something when that works and is implemented
    
    depth averaging setting should be checked
    '''
    nc=Dataset(profile_fil,'r')
    x=nc.groups[cell_name]['ResTime'][:]
    grpd=nc.groups[cell_name][var[0]]
    is_3d= not(len(grpd.shape)==1)
    
    if is_3d:
        lfz=nc.groups[cell_name]['layerface_Z']
        top=lfz[:,0:-1]
        bot=lfz[:,1:]
        nl=lfz.shape[1]-1
        nt=nc.groups[cell_name]['ResTime'].shape[0]
        nv3=1 # number of 3d variables to depth average
        if ref=='sigma':
            depth=top[:,0]-bot[:,-1]
            d1 = bot[:,-1]+ lower *depth
            d2 = bot[:,-1]+ upper *depth
        elif ref == 'elevation':
            d1 = max(np.max(bot[:,-1]),lower)
            d2 = min(np.min(top[:,0]),upper)
        elif ref == 'height':
            d1 = bot[:,-1]+lower
            d2 = min(np.min(bot[:,-1]+upper),upper)
        elif ref == 'depth':
            d1 = max(np.max(top[:,0]-upper),np.max(bot[:,-1]))
            d2 = top[:,0] - lower
        elif ref == 'top':
            d1 = lfz[:,upper]
            d2 = lfz[:,lower]
        elif ref == 'bot':
            d1 = lfz[:,nl-lower-2]
            d2 = lfz[:,nl-upper]
        else :
            NameError("Unspecified depth averaging method given. Check the case \
spelling. Valid methods are 'sigma', 'elevation', 'depth', 'top' and 'bot'")
        d1=np.reshape(d1,(nt,1))
        d2=np.reshape(d2,(nt,1))
        bot = np.maximum(bot,d1)
        top = np.minimum(top,d2)
        frc = np.divide((top-bot),(d2-d1))
        frc = np.maximum(frc,0)
        frc = np.expand_dims(frc,3)
        #process the results
        res = np.zeros([nt,nl,nv3])
        cnt=0
        for vari in var:
            res[:,:,cnt]=nc.groups[cell_name][vari][:]
            cnt=cnt+1
        res = np.multiply(res,frc)
        y = np.sum(res,1)
        
    else:    # assuming it is 2D
        y=nc.groups[cell_name][var][:]
        
    nc.close()
    return x, y
    
def convtime(date_num):
    '''
    This is a bit of a nothing function but it has some use in the fact that is
    shows how you might convert from different pivot dates in python to arrive
    at proper dates.
    '''

    #FV time is in HOURS since 1990
    date_num=np.array(date_num,dtype='datetime64[h]')
    #Work out the conversion to Ordinal times
    tmp1=np.datetime64('1990-01-01') #Tuflow fv zero date
    tmp2=np.datetime64('1970-01-01') # pythons zero date 
    tmp3=tmp1-tmp2
    tmp3=np.timedelta64(tmp3,'h') # choosing to work in hours because they are a good size
    date_num=tmp3+date_num # adding the difference in base dates to get everywhere to the same base

    return  date_num
    
    
        
# Testing 

#in_fil='\\\\blaydos\\scratch2\\B21709\\output\\ARG_2D_020.nc'
#out_fil='\\\\blaydos\\scratch2\\B21709\\output\\ARG_2D_020_PROFILES.nc'

#in_fil='\\\\blaydos\\scratch2\\B22129\\output\\Brunei_001_warmup.nc'
#out_fil='\\\\blaydos\\scratch2\\B22129\\output\\Brunei_001_warmup_SE_test_profiles.nc'
#
#c_ids = get_cell_ids(in_fil,[115.07218,115.07018],[5.157194,5.158294])
#c_ids =np.array(c_ids)
#
##c_ids=np.array([1,4,14768])
#
#
#create_profile_files(in_fil,out_fil,c_ids)
#
#f=plt.figure()
#ax=plt.subplot(1,1,1)
#x,V_y=dave_profiles(out_fil,[('V_y')],'CELL_'+str(c_ids[0]),ref='sigma',lower=0,upper=1)
#x,V_x=dave_profiles(out_fil,[('V_x')],'CELL_'+str(c_ids[0]),ref='sigma',lower=0,upper=1)
#x=convtime(x)
#ax.plot(x,np.hypot(V_x,V_y))
#
##ax.set_ylim(0,1)
##f.autofmt_xdate()
#ax.format_xdata = mdates.DateFormatter('%y-%m-%d %h:%m:%s')


  
    




    





