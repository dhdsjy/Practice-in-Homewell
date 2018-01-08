#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 09:44:33 2017

@author: xuwf

X representing N data points in the D dim
n number of subspace
K number of largest coefficients to pick in order to build the similarity graph,
  typically K = max(subspace dimensions)
"""

import numpy as np

D = 30 # Dimension of ambient space
n = 2 # Number of subspaces
d1 = 1 
d2 = 1 # d1 and d2: dimension of subspace 1 and 2
N1 = 20 
N2 = 20 # N1 and N2: number of points in subspace 1 and 2
X1 = np.random.randn(D,d1) * np.random.randn(d1,N1) # Generating N1 points in a d1 dim. subspace
X2 = np.random.randn(D,d2) * np.random.randn(d2,N2) # Generating N2 points in a d2 dim. subspace
X = np.column_stack([X1,X2]) # not X = [X1,X2]
s1 = 1*np.ones([1,N1])
s2 = 2*np.ones([1,N2])
s = np.column_stack([s1,s2]) #Generating the ground-truth for evaluating clustering results

print len(s1[0]),len(s2[0]),len(s[0])
print s1,s2,s