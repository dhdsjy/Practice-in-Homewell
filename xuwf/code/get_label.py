# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 17:05:01 2017

@author: dell
"""

import numpy as np
import happybase as hb
import pandas as pd
import time

class get_label:
    """
    只针对单个配电柜的获取是否有隐患隐患标签
    
    arguments:
        entityid 为 整数 比如:217 ...
        starttime 为起始位置 字符串 2017-1-1 不包含小时分钟
        endtime 为结束位置 字符串 2017-1-1 不包含小时分钟 获取的隐患类型中不包含时间
        onlyone 为True 代表只获取一个配电柜的隐患情况
        onelabe 为True 代表只获取是否为隐患，不获取具体隐患类型
        
    使用方法
        classGet_label = get_label(217,starttime="2017-1-1",endtime="2017-1-11")
        
        data = classGet_label.onedata
    """
    def __init__(self,entityid,starttime="2017-10-11",endtime="2017-12-11",onlyone=True,onelable=True):

        self.tablename="fault" #版本为单个
        self.ip = '192.168.10.63'
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
        time_list=list()
        for key, value in scan:
    #        print "%s,%s"%(key,value)
            entity=key[0:8]
            fault_time = int(key[8:])-1
            
            time_list.append(fault_time)
            
        l=np.ones([len(time_list),],dtype=np.int16)  
        data[self.entityid]=pd.DataFrame(l,index=time_list)
        connection.close()
        return data
        