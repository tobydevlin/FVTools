# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 09:00:52 2016

@author: Steven.Ettema
"""

import csv
import datetime
import numpy as np

#fil= "C:\\Users\\steven.ettema\\Documents\\Python Scripts\\test.csv"
fil= "L:\\B20020.L.clw_Gladstone_Channel_Duplication\\matlab\\bcs\\sediment\\dredge_bc\\completed_BCs\\western_basin_TSHD.csv"


#def csv_read(fil,nct=1,ncd=0,ncstr=0,nheaderlines=1,fmt_time="%d/%m/%Y %H:%M"):
def csv_read(fil,fmt,nheaderlines=1,fmt_time="%d/%m/%Y %H:%M"):
    #reads in a csv with a pre defined number of columns
    #csv_read
    #fil = path to file to be read
    #fmt formatting string where
        # d is interperated as a date specified as fmt_time
        # f is a float
        # s is a text string
    
    #decode the format string
    nct=0
    ncd=0
    ncstr=0
    FMT=np.ones(len(fmt))
    for aa in range(len(fmt)):
        if fmt[aa]=='f':
            FMT[aa]=1
            ncd=ncd+1
        elif fmt[aa]=='d':
            FMT[aa]=2
            nct=nct+1
        else:
            FMT[aa]=3
            ncstr=ncstr+1

    #be smart and preallocate some memory
    siz=file_len(fil)-nheaderlines
    date=np.empty((nct,siz),dtype='datetime64[us]')
    data=np.empty((ncd,siz),dtype='float32')
    texts=np.empty((ncstr,siz),dtype='S32')
    id1=0
    id2=0
    id3=0    
    # now the file I/O stuff and reading 
    with open(fil,'r') as book:
        page = csv.reader(book,delimiter=',')
        cnt=0
        for aa in range(nheaderlines):
#            if aa==0:
#                for bb in range(len(FMT)):
#                    if FMT[bb]                    
#                    line[bb]
#                    
#                else:
            headers=page.next()
        
                
        for line in page:
            cnt2=0
            for word in line:
                if FMT[cnt2]==1:
                    data[id2,cnt-nheaderlines+1]=float(word)
                    id2=id2+1
                    if id2==ncd:
                       id2=0
                elif FMT[cnt2]==2:
                    date[id1,cnt-nheaderlines+1]=datetime.datetime.strptime(word,fmt_time)
                    id1=id1+1
                    if id1==nct:
                        id1=0
                else:
                    texts[id3,cnt-nheaderlines+1]=word
                    id3=id3+1
                    if id3==ncstr:
                       id3=0 
                cnt2=cnt2+1
            cnt=cnt+1
    return date,data,texts,headers
    
    

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


###################TESTING###########################
#date,data,texts=csv_read(fil,nct=1,ncd=1,ncstr=1)
#import time as time
#tic=time.time()
#date,data,texts,headers=csv_read(fil,nct=1,ncd=7,ncstr=2,nheaderlines=1,fmt_time="%d/%m/%Y %H:%M:%S")
#date,data,texts,headers=csv_read(fil,fmt="dfffffff",nheaderlines=1,fmt_time="%d/%m/%Y %H:%M:%S")
#toc=time.time()
#dif=toc-tic
#print dif