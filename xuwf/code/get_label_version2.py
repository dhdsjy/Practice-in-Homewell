# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 17:05:01 2017

@author: dell
"""

import numpy as np
import happybase as hb
import pandas as pd
import time

class get_label_version2:
    """
    只针对单个配电柜的获取是否有隐患隐患标签
    
    arguments:
        entityid 为 整数 比如:217 ...
        starttime 为起始位置 字符串 2017-1-1 不包含小时分钟
        endtime 为结束位置 字符串 2017-1-1 不包含小时分钟 获取的隐患类型中不包含时间
        onlyone 为True 代表只获取一个配电柜的隐患情况
        onelabe 为True 代表只获取是否为隐患，不获取具体隐患类型
        
    使用方法
        classGet_label = get_label(217,starttime="2017-1-15",endtime="2017-2-15")
        
        data = classGet_label.onedata
        
        data 为字典类型 {entityid:DataFrame(index=time,data=1)}

    """
    def __init__(self,entityid,starttime="2017-10-11",endtime="2017-12-11",onlyone=True,onelable=True):

        self.tablename="fault" #版本为单个
        self.ip = '192.168.10.63'
        self.strStime = starttime
        self.strEtime = endtime
        self.entityid="%08d"%entityid
        self.starttime="%d"%time.mktime(time.strptime(starttime,"%Y-%m-%d"))
        self.endtime="%d"%time.mktime(time.strptime(endtime,"%Y-%m-%d"))
        if onlyone==True and onelable==True:
            self.onedata=self.get_fault()
        
    def get_fault(self):
        #该方法只获取row以及
        connection=hb.Connection(self.ip)
        table=connection.table(self.tablename)
        scan=table.scan(row_start=self.entityid+self.starttime,
                        row_stop=self.entityid+self.endtime,
                        include_timestamp=False,batch_size=10000)
        
        data={}
        
        #格式转换成timestamp
        date = pd.date_range(self.strStime,self.strEtime,freq='D')
        
        ll=np.arange(int(self.starttime),int(self.endtime),86400)
        
        print date
        
        store = pd.DataFrame(data=date[:-1],index=ll)
        
        store.rename(columns={0:"time"},inplace=True)
        
        store["label"]=0
        
        for key, value in scan:
    #        print "%s,%s"%(key,value)
            entity=key[0:8]
            fault_time = int(key[8:])-1
            
            store.ix[fault_time,'label']=1
            #time_list.append(fault_time)
            
        #l=np.ones([len(time_list),],dtype=np.int16)
        #data[self.entityid]=pd.DataFrame(l,index=time_list)
        data[self.entityid]=store
        connection.close()
        return data #data['00000217'].label
if __name__=='__main__':    
    classGet_label = get_label_version2(95401,starttime="2017-9-7",endtime="2017-11-28")
    data = classGet_label.onedata
    data['00095401'].label.to_csv('/home/xuwf/xuwf/data/label_for_95401_.csv',index=False,header=False)