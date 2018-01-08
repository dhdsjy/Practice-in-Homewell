# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 09:05:02 2017

@author: dell
"""

import numpy as np
import pandas as pd
import heapq
from scipy.optimize import leastsq
import scipy
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import time


class fsc(object):
    
    def __init__(self,data,threholdvalue):
        #定义关系程度,作为子空间选基的参数
        self.threholdvalue=threholdvalue
        #transdata列数据为当日时刻，行数据为时间，其行index对应由self.index决定
        self.transdata=self.trans(data)
        
        self.xnum=self.transdata.shape[0]
        #DTW的限制边长为2，相当于半个小时
        self.timestamps=2
        #计算相似矩阵B
        self.B=self.symmetrix()
        #聚多少类
        self.n_cluster=3
        
        self.speccluster(maxnum=3)
        
    
    def trans(self,data):
        #转化成数据或list,确保数据是从凌晨开始到晚上24点的维度
        if isinstance(data,dict):
            #选取最小两个元素判断数列长度
            length=len(data)
            arr=heapq.nsmallest(2,data)
            step=arr[1]-arr[0]
            gap=24*60*60/step
            a=pd.DataFrame(data.items(), columns=['timestamp', 'value_ac']).sort_values('timestamp').reset_index(drop=True)
            #作为分类标准下的index对应的时间 self.index
            index=np.linspace(0,length,length/gap,endpoint=False)
            timevalue=a['timestamp'][index]
            timevalue=timevalue.reset_index(drop=True)
            self.index=timevalue
            #整合数据
            transdata=np.asarray(a['value_ac']).reshape(length/gap,gap)
            
            return transdata
        
    #forevector 为匹配向量，1.如果解非整数解使用frank-wolfe算法计算，
    #2.如果解整数解，使用最近一个小时即4*2+1个长度的数据进行匹配,先做求整数解
    def DTWf(self,forevector,lastvector,dayindex,timestamps=4):
        #解整数解
        daylen=len(forevector)
#        daynum=self.transdata.shape[0]
        #z欧式距离最小的那个元素
        bestz=[]
        newarray=[]
        for i in np.arange(0,daylen):
            distance=0

            y=forevector[i]
            count=0
            minarry=0
            minz=0
            minvalue=0
            start=i-timestamps
            #为了时间的先后顺序,保证数据的连续性与次序
            if len(bestz)>0 and bestz[-1]>start:
                start=bestz[-1]
            end=i+timestamps+1
            if dayindex==0 and start<0:
                start=0
            if dayindex+1==self.xnum and end>=daylen:
                end=daylen
            
            
            for j in np.arange(start,end):
                count+=1
                if j<0:
                    minarry=self.transdata[dayindex-1][j]
                    distance2=np.abs(y-minarry)
                    
                elif j>=daylen:
                    index=j-daylen
                    minarry=self.transdata[dayindex+1][index]
                    distance2=np.abs(y-minarry)

                else:
                    minarry=lastvector[j]
                    distance2=np.abs(y-minarry)

                if count==1:
                        distance=distance2
                        minz=j
                        minvalue=minarry
                else:
                    if distance>distance2:
                        distance=distance2
                        minz=j
                        minvalue=minarry
            
            bestz.append(minz)
            newarray.append(minvalue)           
        r=scipy.corrcoef(forevector,newarray)[0,1]    
        return r,bestz,newarray

    
    #提取最靠近残差项的数据，并作DTW 
    def maxangle(self,Resident,set,timestamps=4):
        r=0

        bestz=[]
        minarr=[]
        getmaxindex=0
        getbestz=[]
        getminarr=[]
        for i in set:
            #计算最优化的角度
            r1,bestz,minarr=self.DTWf(Resident,self.transdata[i],i,timestamps=timestamps)
            if r1>r and r1>self.threholdvalue:
                r=r1

                getmaxindex=i
                getbestz=bestz
                getminarr=minarr
        
        if r>self.threholdvalue:
            return True,getmaxindex,getbestz,getminarr
        else:
            return False,-1,-1,-1    
        
    def symmetrix(self):
        
        nvector=len(self.index)
        set1=set(np.arange(0,nvector))
        B=np.zeros((self.xnum,self.xnum))

        for i in set1:
            settotal=set(np.arange(0,nvector))
            #初始化子空间，以及用过的编号J，以及残差项
            
            forevector=self.transdata[i]
#            BestSubspace=[]
            J=set([])
            J.add(i)
            Resident=forevector
            #choice the best angle
            #每次获取相似度最大的一个项目
            getmaxindex=0
            getbestz=dict()
            getminarr=dict()
            
            while True:
                iftrue,getmaxindex,bestz,minarr=self.maxangle(Resident,settotal-J,timestamps=self.timestamps)
                if not iftrue:
                    break
                getminarr[getmaxindex]=minarr
                getbestz[getmaxindex]=bestz
                
                ll=self.pcasubspace(forevector,getminarr)
                Resident=ll['res']
                for ind in ll['coef'].index:
                    B[i,ind]=ll['coef'][ind]
                J.add(getmaxindex)
                
        return B
                    
    def pcasubspace(self,forevector,lastvector):
        #按照论文的算法，这里并没有寻找到基的过程，而是寻找最优曲线的y的过程
        y=forevector
        if isinstance(lastvector,dict):
            ret=dict()
            loopn=len(lastvector)
            keyvalue=np.array(lastvector.keys())
            
            def residuals(p):
                res=y.copy()
                count1=0
                for k in p:
                    res=res-k*np.array(lastvector[keyvalue[count1]])
                    count1+=1
                return res
            
            r=leastsq(residuals,np.zeros(loopn))
            
            res2=residuals(r[0])
            ret['coef']=pd.Series(r[0],index=keyvalue)
            ret['res']=res2#返回残差项
#            ret['coef']=r[0]#返回系数项                 
#            
#            ret['keyvalue']=keyvalue#返回定的数列值
            return ret
        else:
            raise TypeError,("The lastvector must be a list")
            
   #maxnum代表取前几的数据进行聚类
    def speccluster(self,maxnum=2):
        #旋转矩阵B与其转置矩阵的和组成A对称矩阵，其对角线均为0
        A=self.B+self.B.T
        
        D=np.sum(A,axis=0)
        #为了能够不除于0，需要转换
        for y,n in enumerate(D):
            if n==0:
                D[y]=np.float("inf")

#        DnegMetrix=np.diag(1/sqrt(D))
        #拉普拉斯领接矩阵L sym
#        L=np.dot(np.dot(DnegMetrix,A),DnegMetrix)
        #拉普拉斯领接矩阵L rw,点与点之间的关系程度由此图给定
        L=np.diag(np.ones(A.shape[0],dtype='f'),0)-np.dot(np.diag(1/D),A)
        
        lamda,SpeVector=np.linalg.eig(L)
        
        a=pd.DataFrame(lamda)
        a=a.sort_values(by=0,ascending=False)
        #计算方差选取前二大的值
        self.lamdavalue=a
        c=a.diff(-1).sort_values(by=0,ascending=False)
        #定义特征最大值的数量,定义最大值如果数量超过1个，就用超过的数量，否则，选取两个最大的稳定向量
        specvaluenum=np.count_nonzero(c==np.nanmax(c))
#        self.sepcccc=specvaluenum
        if specvaluenum>1:
            b=c[0:specvaluenum]
        else:
            b=c[0:maxnum]
        
        index=[]
        for x in b.index:
                index.append(x)
        #需要聚类的特征向量
        self.clustervector=SpeVector.T[index]
        
        self.clusterY(self.clustervector)
        

#        a=list(lamda)
#        for x in a:
            
        #需要聚类的特征向量
#        b=pd.Series(SpeVector.T[2])
#        plt.scatter(b.index,b)

        
    def clusterY(self,data):
        dn=data.shape[0]
        list=[]
        for n in xrange(dn):
            list.append(data[n])
        kdata=np.array(list).T
        #Kmeans算法
        kmeans=KMeans(n_clusters=self.n_cluster,n_jobs=4,max_iter=500)#聚5类，并发4，最大迭代500    
        #
        kmeans.fit(kdata)
#        #统计各个类别数量
        self.r1 = pd.Series(kmeans.labels_).value_counts()
#        #找出聚类中心
        self.r2 = pd.DataFrame(kmeans.cluster_centers_)
#        #输出，聚类中心与类别
        self.r = pd.concat([self.r2, self.r1], axis = 1)
#        #聚类类别
        categoryvector=pd.Series(kmeans.labels_)
        
        dayname=pd.DataFrame([fsc1.index,categoryvector]).T
                            
        self.Y=pd.DataFrame(np.array([map(lambda x:time.strftime('%Y-%m-%d',time.localtime(x)),dayname['timestamp']),categoryvector])).T
#        if dn==3:
#            self.plot3d(data,categoryvector)
#            self.plot2d(data,categoryvector)
#        if dn==2:
#            self.plot2d(data,categoryvector)
#        return Y
    #画3d散点图
    def plot3d(self,data,categoryvector):  
        J=set(categoryvector)
        fig = plt.figure(num=1, figsize=(13, 6))
        ax = Axes3D(fig)
        scat=[".","*","v","+","s",'x']
        color=['b','y','r','g','black','p']  
        dd=pd.DataFrame(data.T,categoryvector)     
        for jj in J:
            
            ax.scatter(dd.ix[jj,0], 
                       dd.ix[jj,1], 
                       dd.ix[jj,2],c='b',marker=scat[jj],s=50)

        plt.show()
        plt.close('all') 
    #画2d散点图
    def plot2d(self,data,categoryvector):  
        J=set(categoryvector)
        fig = plt.figure(num=1, figsize=(13, 6))
        scat=[".","*","v","+","s",'x']
        color=['b','y','r','g','black','p']  
        dd=pd.DataFrame(data.T,categoryvector)     
        for jj in J:
            
            plt.scatter(dd.ix[jj,0], 
                       dd.ix[jj,1], 
                       c='b',marker=scat[jj],s=50)
        plt.show()
        plt.close('all') 
        
if __name__ == '__main__':
        ls=dict()
        for x in np.linspace(0.5,1,100):
            
            threholdvalue=x
            fsc1=fsc(llll,threholdvalue)
            B2=fsc1.B
            A2=B2+B2.T
            D2=pd.Series(np.sum(A2,axis=0))
            #选出无法关联的用电日期
            
            ls[threholdvalue]=D2.index[D2==0]
#        fsc1.Y.ix[D2.index[D2==0]]
#        plt.plot(fsc1.transdata[D2.index[D2==0]].T)
#        plt.plot(fsc1.transdata[D2.index[D2!=0]].T)
        
    #测试
#    def DTWf(forevector,lastvector,dayindex,timestamps=4):
#        #解整数解
#        daylen=len(forevector)
#        daynum=fsc1.transdata.shape[0]
#        #z欧式距离最小的那个元素
#        bestz=[]
#        newarray=[]
#        for i in np.arange(0,daylen):
#            distance=0
#
#            y=forevector[i]
#            count=0
#            minarry=0
#            minz=0
#            minvalue=0
#            start=i-timestamps
#            if len(bestz)>0 and bestz[-1]>start:
#                start=bestz[-1]
#            end=i+timestamps+1
#            if dayindex==0 and start<0:
#                start=0
#            if dayindex+1==daynum and end>=daylen:
#                end=daylen
#            
#            for j in np.arange(start,end):
#                count+=1
#                if j<0:
#                    minarry=fsc1.transdata[dayindex-1][j]
#                    distance2=np.abs(y-minarry)
#                    
#                elif j>=daylen:
#                    index=j-daylen
#                    minarry=fsc1.transdata[dayindex+1][index]
#                    distance2=np.abs(y-minarry)
#
#                else:
#                    minarry=lastvector[j]
#                    distance2=np.abs(y-minarry)
#
#                if count==1:
#                        distance=distance2
#                        minz=j
#                        minvalue=minarry
#                else:
#                    if distance>distance2:
#                        distance=distance2
#                        minz=j
#                        minvalue=minarry
#            
#            bestz.append(minz)
#            newarray.append(minvalue)           
#            
#        return bestz,newarray
#    
#    a1=fsc1.transdata[19]
#    a2=fsc1.transdata[24]
#    scipy.corrcoef(a1,a2)
#    aa,bb=DTWf(a1,a2,24)
#    scipy.corrcoef(a1,bb)
#    plt.plot(bb)
#    plt.plot(a1)
#    plt.plot(a2)