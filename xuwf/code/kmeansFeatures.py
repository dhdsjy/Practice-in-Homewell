#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 16:10:37 2017

@author: xuwf
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score 
from sklearn.metrics import calinski_harabaz_score

features = pd.read_csv('/home/xuwf/xuwf/data/data_for_fsc/process_and_result_for_experiment/fscwraped_3features_82days_versionABC2.csv',header = None,sep='\t')
labels = pd.read_csv('/home/xuwf/xuwf/data/data_for_fsc/ready_for_experiment/label_for_95401_.csv',header = None)

X = features.as_matrix()
kmeans = KMeans(n_clusters=18,random_state=0).fit(X)# fscwrapedABC n=3 0.225 n=23 0.289 ##fsceulicABC n=23 0.2866 n=36 0.317 # fsceulicA n=9 0.2986 #euliB n=5 0.2622
pre_labels = kmeans.labels_# eulicC n=14 0.3278 wraped C n=38 0.338
print 'silhouette_score is :',silhouette_score(X,pre_labels,metric='euclidean')
print 'calinski_harabaz_score is :',calinski_harabaz_score(X, pre_labels)# more better more big


# Visual

label0 = np.where(pre_labels==0)
label1 = np.where(pre_labels==1)
label2 = np.where(pre_labels==2)
label3 = np.where(pre_labels==3)
label4 = np.where(pre_labels==4)
ax = plt.subplot(121,projection='3d')
ax.scatter(features.iloc[label0][0],features.iloc[label0][1],features.iloc[label0][2],c='r',marker='o',label = 'class1')
ax.scatter(features.iloc[label1][0],features.iloc[label1][1],features.iloc[label1][2],c='g',marker='^',label = 'class2')
#ax.scatter(features.iloc[label2][0],features.iloc[label2][1],features.iloc[label2][2],c='m',marker='s',label = 'class3')
#ax.scatter(features.iloc[label3][0],features.iloc[label3][1],features.iloc[label3][2],c='k',marker='x',label = 'class4')
#ax.scatter(features.iloc[label4][0],features.iloc[label4][1],features.iloc[label4][2],c='c',marker='h',label = 'class5')
ax.set_title('After clustering')
ax.legend(loc=3)
ax.set_xlabel('Dimension 1') #plt.xlabel('Dimension 1')
ax.set_ylabel('Dimension 2')#plt.ylabel('Dimension 2')
ax.set_zlabel('Dimension 3')#plt.zlabel('Dimension 3')

ground_label0 = labels[labels[0]==0].index.tolist()
ground_label1 = labels[labels[0]==1].index.tolist()
ax = plt.subplot(122,projection='3d')
ax.scatter(features.iloc[ground_label0][0],features.iloc[ground_label0][1],features.iloc[ground_label0][2],c='b',marker='*',label = 'class1')
ax.scatter(features.iloc[ground_label1][0],features.iloc[ground_label1][1],features.iloc[ground_label1][2],c='y',marker='d',label = 'class2')
ax.set_title('Before clustering')
ax.legend(loc=3)
ax.set_xlabel('DimensionG 1') #plt.xlabel('Dimension 1')
ax.set_ylabel('DimensionG 2')#plt.ylabel('Dimension 2')
ax.set_zlabel('DimensionG 3')#plt.zlabel('Dimension 3')