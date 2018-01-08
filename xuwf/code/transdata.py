#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 13:32:34 2017

@author: xuwf
"""

import pandas as pd
import numpy as np

data = pd.read_csv('/home/xuwf/xuwf/data/data_for_fsc/ready_for_experiment/C_current_12month_for_entity95401.csv')
data = data.drop('timestamp',axis=1)

def transdata(data):
    
    date_rng = pd.date_range('20170907','20171128',freq='1s')# notes the parma freq='1s'
    
    # timestamp to string
    date_string = []
    def datetime_toString(dt):
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    for i in date_rng:
        a = datetime_toString(i)
        date_string.append(a)
        
    new_data = pd.DataFrame(date_string)
    new_data.columns = ['new_date']
    merge_data = pd.merge(new_data,data,left_on='new_date',right_on='date',how = 'left')
    merge_data['value'].fillna(method='bfill',axis=0,inplace=True)
    merge_data['value'].fillna(method='pad',axis=0,inplace=True)
    merge_data.drop(['date'],axis=1,inplace=True)
    merge_data.set_index('new_date')
    
    gap = 24*60*60#24*60*60
    length = len(merge_data)
    index = map(int,np.linspace(0,length,length/gap,endpoint=False))
    row_index = merge_data['new_date'][index]#  Select the data for each day as a row index
    row_index.reset_index(drop=True)
    transdata = np.asarray(merge_data['value'][:len(merge_data)-1]).reshape(int(length/gap),gap)
    transdata = pd.DataFrame(transdata,index=row_index)
    
    return transdata
a = transdata(data)
    
dataTransed =transdata(data)
dataTransed_sample = dataTransed.sample(frac=0.017,axis=1)
dataTransed_sample.to_csv('/home/xuwf/xuwf/data/data_for_fsc/ready_for_experiment/Ctest_noindex.csv',header=False,index=False)
    
    