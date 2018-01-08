#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 16:19:32 2017

@author: xuwf
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import sqrt
import sys
#
#def dtw(num1,num2):
#    num1Len = len(num1)
#    num2Len = len(num2)
#    cost = 0
#    
#    # construct a num1Len * num2Len matrix
#    mat = np.zeros([num1Len,num2Len],int)
#    for i in range(0,num1Len):
#        for j in range(0,num2Len):
#            mat[i,j] = sys.maxint
#    mat[0,0]=0
#    
#    for i in range(1,num1Len):
#        for j in range(1,num2Len):
#            cost = sqrt((num1[i] - num2[j])**2)
#            mat[i,j] = cost + min(mat[i-1,j],mat[i,j-1],mat[i-1,j-1])
#       
#       
#       
#       
#    return mat[num1Len-1,num2Len-1]
#num1 = [1,2,3,4]
#num2 = [1,2,7,4,5]
#print dtw(num1,num2)

def distance(x,y):
    return sqrt((x - y)**2)

def dtw(X,Y):
     
     #M=[[distance(X[i],Y[j]) for j in range(len(Y))] for i in range(len(X))]
     # Control the distortion range
     M = np.zeros([len(X),len(Y)])
     for i in range(len(X)):
         for j in range(len(Y)):
             
             if abs(i-j) < 2:
                 M[i,j] = distance(X[i],Y[j])
             else:
                 M[i,j] = sys.maxint
     print M
            
            
             
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
 
#data = pd.read_csv('/home/xuwf/xuwf/data/C_current_0.csv')
#X = [i for i in data['value'][:1000]]
#Y = [j for j in data['value'][1000:2000]]
X=[1,2,3,4]
Y=[1,2,7,4,5]
print dtw(X,Y)

#plt.subplot(211)
#plt.plot(data.value[:1000])
#plt.subplot(212)
#plt.plot(data.value[1000:2000])
#print dtw(X,Y)
 


