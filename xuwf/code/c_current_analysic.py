#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 10:43:03 2017

@author: xuwf
"""
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import SpectralClustering 
from math import ceil,sqrt
from sklearn import metrics




# transform the data to a comfortable form
def transdata(merge_data):
    gap = 24*60*60
    length = len(merge_data)
    index = map(int,np.linspace(0,length,length/gap,endpoint=False))
    row_index = merge_data['new_date'][index]#  Select the data for each day as a row index
    row_index.reset_index(drop=True)
    transdata = np.asarray(merge_data['value'][:2073600]).reshape(int(length/gap),gap)
    transdata = pd.DataFrame(transdata,index=row_index)
    return transdata

def distance(x,y):
    return sqrt((x - y)**2)

def dtw(X,Y):
     
     M = np.zeros([len(X),len(Y)]) # a large matrix lead to a memoryError
     for i in range(len(X)):
         for j in range(len(Y)):
             
             if abs(i-j) < 450: # 15min
                 M[i,j] = distance(X[i],Y[j])
             else:
                 M[i,j] = sys.maxint
     l1=len(X)
     l2=len(Y) 
     D=[[0 for j in range(l2+1)] for i in range(l1+1)]
     D[0][0]=0 
     for i in range(1,l2+1):
         D[0][i]=sys.maxint
     for j in range(1,l1+1):
         D[j][0]=sys.maxint
     for i in range(1,l1+1):
         for j in range(1,l2+1):
             D[i][j] = M[i-1][j-1] + min(D[i-1][j],D[i][j-1],D[i-1][j-1])
     return D[l1][l2]
 
def constructB(trans):
    #B = np.eye(len(trans))
    for i in range(len(trans)):
        for j in range(i,len(trans)):
            B[i,j] = dtw(trans.values[i],trans.values[j])
    #print B
    return B
             
   
     
     
     


    
if __name__ =='__main__':
    data = pd.read_csv('/home/xuwf/xuwf/data/C_current_2.csv')
    date_rng = pd.date_range('15/01/2017','11/25/2017',freq='1s')
    
    # timestamp to string
    date_string = []
    def datetime_toString(dt):
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    for i in date_rng:
        a = datetime_toString(i)
        date_string.append(a)
    
    # merge data and fill missing data
    new_data = pd.DataFrame(date_string)
    new_data.columns = ['new_date']
    merge_data = pd.merge(new_data,data,left_on='new_date',right_on='date',how = 'left')
    merge_data['value'].fillna(method='bfill',axis=0,inplace=True)
    merge_data['value'].fillna(method='pad',axis=0,inplace=True)
    merge_data.drop(['date','timestamp'],axis=1,inplace=True)
    merge_data.set_index('new_date')
    transdata = transdata(merge_data)
    transdata_sample = transdata.sample(frac=0.01,axis=1)
    B = np.eye(len(transdata_sample))
    print constructB(transdata_sample)
    print B
    
    
    # origin code  not work :a bad direction
#    sc = SpectralClustering(n_clusters = 3, eigen_solver = 'arpack',random_state = 10,
#                            gamma = 1.0, affinity='rbf',assign_labels='kmeans')
#    
#    y_pred = sc.fit_predict(transdata)
#    aff_mat = sc.affinity_matrix_
#    aff_lab = sc.labels_
#    param = sc.get_params
#    print 'CH score %.2f',metrics.calinski_harabaz_score(transdata,y_pred)
#    
    
    

#new_data.merge(data,left_on='date',right_on='new_date')

#new_value = 


#data.head()

#plt.plot(data.value)



#sample_data = data.sample(frac = 0.001)
#sample_data.columns = ['date','timestamp','value']

# a simple scatter //not work how to visualize the data?
#sample_data.plot.scatter(x=sample_data['date'],y=sample_data['value'])

# Divide each day into 24 hours and observe the changes of each day
