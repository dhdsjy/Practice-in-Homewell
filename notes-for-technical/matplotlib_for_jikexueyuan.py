#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 16:40:15 2017

@author: xuwf
"""
import numpy as np
import matplotlib.pyplot as plt

# V! simple figure
x = np.linspace(0,10,1000)# start end nums it's different for arange(start end step)
y = np.sin(x)
z = np.cos(x)
plt.figure(figsize=(8,6))
plt.plot(x,y,label='sin(x)')
plt.plot(x,z,'b--',label='cos(x)')
plt.xlabel('Time(s)')
plt.ylabel('Values')
plt.title('sin(x)&cos(x)')
plt.ylim(-1.2,1.2)
plt.legend()# show the legend
plt.show()
fig = plt.gcf()
ax = plt.gca()
print fig
print ax

# V2 subplot

for idx,color in enumerate('rgbyck'):
    plt.subplot(320+idx+1,axisbg=color)
plt.show()

# V3 log axis
w = np.linspace(0.1,1000,1000)
p = np.abs(1/(1+0.1j*w))

plt.subplot(221)
plt.plot(w,p,linewidth=2)
plt.ylim(0,1.5)

plt.subplot(222)
plt.semilogx(w,p,linewidth=2)
plt.ylim(0,1.5)

plt.subplot(223)
plt.semilogy(w,p,linewidth=2)
plt.ylim(0,1.5)

plt.subplot(224)
plt.loglog(w,p,linewidth=2)
plt.ylim(0,1.5)

# V4 bar matplotlib.pyplot.bar(left, height, width=0.8, bottom=None, hold=None, **kwargs)
# left        每个柱x轴左边界
# bottom      每个柱y轴下边界
# height      柱高度(Y轴方向)
# width       柱宽度(X轴方向)
# 以上参数可以设置为数值或者list 但要保证如果为list, len(list)要一致
#绘制的方形为:
#    X: left   --- left+width
#    Y: bottom --- bottom+height
data = np.loadtxt('/home/xuwf/hw/Practice-in-Homewell/notes-for-technical/data/test0.csv')
width = (data[1,0]-data[0,0])*0.4
plt.figure()
plt.bar(data[:,0]-width,data[:,1],width,label='person')
plt.xlim(-width,40)
plt.xlabel('Age')
plt.ylabel('Num')
plt.legend()
plt.show()

# V5 Scatter
plt.figure()
x = np.random.random(100)
y = np.random.random(100)
plt.scatter(x,y,s = x*1000,c=y,marker=(5,1),lw=2,facecolor='none')
plt.xlim(0,1)
plt.ylim(0,1)
plt.show()

# V6 3d
import mpl_toolkits
from mpl_toolkits.mplot3d import Axes3D

np.random.seed(42)
n_samples = 500
dim = 3
samples = np.random.multivariate_normal(np.zeros(dim),np.eye(dim),n_samples)
for i in range(samples.shape[0]):
    r = np.power(np.random.random(),1.0/3.0)
    samples[i]*=r/np.linalg.norm(samples[i])
upper_samples = []
lower_samples = []
for x,y,z in samples:
    if z>3*x+2*y-1:
        upper_samples.append((x,y,z))
    else:
        lower_samples.append((x,y,z))
fig = plt.figure('3D scatter plot')
ax = fig.add_subplot(111,projection='3d')# or ax = Axes3D(fig)
uppers = np.array(upper_samples)
lowers = np.array(lower_samples)
ax.scatter(uppers[:,0],uppers[:,1],uppers[:,2],c='r',marker='o')
ax.scatter(lowers[:,0],lowers[:,1],lowers[:,2],c='k',marker='^')