# -*- coding: utf-8 -*-
"""
Created on Fri Jan 08 09:42:03 2016

@author: Steven.Ettema
"""
import datetime as dt

def convtime(date_num):

    #FV time is in HOURS since 1990
    date_num=date_num*60*60 #convert to seconds
    #Work out the conversion to Ordinal times
    tmp1=dt.datetime(1990,1,1,0,0,0)
    tmp2=dt.datetime(1970,1,1,0,0,0)
    tmp3=tmp1-tmp2
    tmp3=tmp3.total_seconds()
    date_num=dt.datetime.utcfromtimestamp(tmp3+date_num)

    return  date_num
    