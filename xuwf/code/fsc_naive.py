#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 16:15:13 2017

@author: xuwf
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.linalg.misc import norm

data = pd.read_csv('/home/xuwf/xuwf/data/C_current_0.csv')

for i in range(len(data)):
    F = set() 
    J = set()
    J.add(i)
    R1 = data['value'][i]
    l = 1
    if j not in J:
        while max(np.dot(Rl,data['value'][j]/(norm(Rl)*norm(data['value'][j])))) > 0.1:
        