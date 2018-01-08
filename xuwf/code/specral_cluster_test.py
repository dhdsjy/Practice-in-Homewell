# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 16:15:13 2017

@author: xuwf
"""
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import SpectralClustering 
from sklearn import datasets
from sklearn import metrics
from math import ceil

# construct a customized affinity matrix


#X,y = datasets.make_blobs(n_samples=500,n_features=6,centers=5,
#                          cluster_std=[0.4,0.3,0.4,0.3,0.4],random_state=10)
data = pd.read_csv('/home/xuwf/xuwf/data/C_current_0.csv')
data_matrix = data.values[:,1:3]

# origin code  not work :a bad direction
sc = SpectralClustering(n_clusters = 2, eigen_solver = 'arpack',random_state = 10,
                        gamma = 1.0, affinity='rbf',assign_labels='kmeans')

y_pred = sc.fit_predict(data_matrix)
aff_mat = sc.affinity_matrix_
aff_lab = sc.labels_
param = sc.get_params
print 'CH score %.2f',metrics.calinski_harabaz_score(data_matrix,y_pred)
#print 'Silhouette coefficient is %.2f',metrics.silhouette_score(data_matrix,y_pred,metric='euclidean')

## Adjustment parameters
#
## define a function to loop float
#def floatrange(start,end,step):
#    nums_step = int(ceil((float(end)-float(start))/step))
#    return [ start + i*step for i in range(nums_step)]
#
#num_clusters = range(3,12)
#range_gamma = floatrange(0.1,1,0.1)#range(0.1,1,0.1)
#resx = []
#resy = []
#resz= []
#for i in num_clusters:
#    for j in range_gamma:
#        sc = SpectralClustering(n_clusters = i, eigen_solver = 'arpack',random_state = 10,
#                        gamma = j, affinity='rbf',assign_labels='kmeans')
#        y_pred = sc.fit_predict(X)
#        resx.append(i)
#        resy.append(j)
#        resz.append((metrics.calinski_harabaz_score(X,y_pred)/10000))
#        
#        print 'i is %d, j is %.2f,CH score %.2f' % (i,j,metrics.calinski_harabaz_score(X,y_pred))
##print aff_mat
##print aff_lab
##print param
#
## plot 3D
#from mpl_toolkits.mplot3d import Axes3D
#fig = plt.figure()
#ax = fig.add_subplot(111,projection='3d')
#x = resx
#y = resy
#z = resz
#ax.scatter(x,y,z,c='red',alpha=0.4)
#ax.set_xlabel('clusters')
#ax.set_ylabel('gamma')
#ax.set_zlabel('eval')
#plt.show()

    
    