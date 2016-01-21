# -*- coding: utf-8 -*-
"""
Created on Fri Jan 08 09:42:03 2016

@author: Steven.Ettema
"""
import datetime as dt


def convtime(fvtime):

    #FV time is in HOURS since 1990
    date_num = fvtime * 60 * 60  # convert to seconds
    #Work out the conversion to Ordinal times
    tmp1 = dt.datetime(1990, 1, 1, 0, 0, 0) - dt.datetime(1970, 1, 1, 0, 0, 0)
    date_num = dt.datetime.utcfromtimestamp(tmp1.total_seconds() + date_num)
    return  date_num
