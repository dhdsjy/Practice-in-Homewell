# -*- coding: utf-8 -*-
"""
Created on Mon May 22 09:57:51 2017

@author: zhangll
"""
import happybase
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time

class GetData:
    
    def __init__(self,name='entity'):
        
        self.name=name
        
        
    def getall(self,table='casecheck'):
        connection=happybase.Connection('192.168.10.63')
        table=connection.table(table)
        s=table.scan(include_timestamp=True)
        t=[]
        data=[]
        ts=[]
        for i,j in s:
            t.append(int(i[8:]))
            data.append(float(j.values()[0][0]))
            ts.append(j.values()[0][1])
        return data,t,ts
        
    def gethistorydata(self,entityid,starttime,endtime,sensorno=-1):
        
    #创建与hbase的链接
            if self.name=='historydata':
            
                connection=happybase.Connection('192.168.10.63')
                
                table=connection.table('historydata')
                #对输入数据进行格式处理
                
                
                start_time=time.mktime(time.strptime(starttime,'%Y-%m-%d %H:%M:%S'))
                end_time=time.mktime(time.strptime(endtime,'%Y-%m-%d %H:%M:%S'))   
                
                
                
                standardrow='%08d'%entityid
                startrow=standardrow+str(start_time)
                stoprow=standardrow+str(end_time)
                startrow= startrow.encode(encoding="utf-8")
                stoprow= stoprow.encode(encoding="utf-8")
            #    timestamp=sensorno+1
                #获取数据到生成器并取出并按格式保存到df
                s=table.scan(row_start=startrow,row_stop=stoprow,timestamp=sensorno+1,include_timestamp=True)
                
                t=[]
                data=[]
                ts=[]
                for i,j in s:
                    t.append(int(i[8:]))
                    data.append(float(j.values()[0][0]))
                    ts.append(j.values()[0][1])
                dic={'timestamp':t,'value':data,'ts':ts}
                
                df=pd.DataFrame(dic)
                #删除错误数据
                df=df.ix[df.ts==sensorno]
                
                df=df.drop(['ts'],axis=1)
                
                df=df.sort_values(['timestamp'])
    
                df=df.reset_index(drop=True)
                
                #修改时间格式到index
                stime=[]
                [stime.append(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(i))) for i in df.timestamp]
                df.index = pd.to_datetime(stime)
                
                connection.close()
                
                return df
    
    
    def getentitydata():
        
        connection=happybase.Connection('192.168.10.63')
        
        table=connection.table(self.name)

        s=table.scan(columns=['I:Left', 'I:Level','I:Right','f:Parentid','f:EntityLnglat','f:OE'])
        t1={}
        
        for key, data in s:
            #print key, data
            t1[key]=data
        
        key_value=list(t1.keys())   
        
        value_list=list(t1.values())
        
        frlist=pd.DataFrame(value_list)
        
        frlist2=pd.DataFrame(key_value)
        
        frlist['entityid']=frlist2
              
        connection.close()

        return frlist
    def getsensorname():
        
        connection=happybase.Connection('192.168.10.63')
        
        table=connection.table(self.name)
    
    
def transdata(data1_ent_mid,data2):

     ent_2=pd.merge(data1_ent_mid,data2.ix[:,['f:Parentid', 'entityid']],how= 'inner',left_on='f:Parentid',right_on='entityid')     
           
     ent_3=ent_2.ix[:,['f:EntityLnglat','I:Level','f:Parentid_y', 'entityid_x']]
                
     ent_3.rename(columns={'f:Parentid_y':'f:Parentid', 'entityid_x':'entityid'}, inplace = True)
     
     return ent_3
    
    
    


def creattable():
     connection=happybase.Connection('192.168.10.63')
     connection.create_table('parentchildid',
                                   {'f':dict(max_versions=1)
                                           })
     connection.close()
def putdata(data):
    connection=happybase.Connection('192.168.10.63')
    
    table=connection.table('parentchildid')
    
    bat=table.batch()
    
    for danyuan in zip(data['I:Level'],data['f:EntityLnglat'],data['new_col']):
        
        lnglat=danyuan[1]
        
        if pd.isnull(danyuan[1]):
            
            lnglat=""
        
        bat.put(danyuan[2],{'f:Level':danyuan[0],'f:EntityLnglat':lnglat})
    
    bat.send()
    
    connection.close()

    

def do_something(x, y):
    return x + y

if __name__ == "__main__":
    
    starttime=time.time()
    
    t=getentitydata()
    
    org_l1=t[(t['I:Level']=='1')&(t['f:OE']!='ENT')]
    org_l2=t[(t['I:Level']=='2')&(t['f:OE']!='ENT')]
    org_l3=t[(t['I:Level']=='3')&(t['f:OE']!='ENT')]
    org_l4=t[(t['I:Level']=='4')&(t['f:OE']!='ENT')]
    
    ent_l1=t[(t['f:OE']=='ENT')]
    cc=pd.merge(org_l2,org_l1[org_l1.columns[5:]],left_on='f:Parentid',right_on='entityid',how='outer')
    
    #循环次数
    ent_level_max=max(np.array(list(ent_l1['I:Level']),dtype=np.int64))+1
    ent_level_min=min(np.array(list(ent_l1['I:Level']),dtype=np.int64))
    #对遍历的数组进行添加
    t1=[]

    
    t3=org_l4      
    t3['new_col'] = map(lambda x, y: do_something(x, y) , t3['f:Parentid'], t3['entityid']) 
    putdata(t3)
    
    t3=org_l3      
    t3['new_col'] = map(lambda x, y: do_something(x, y) , t3['f:Parentid'], t3['entityid']) 
    putdata(t3)
    
    t3=org_l2      
    t3['new_col'] = map(lambda x, y: do_something(x, y) , t3['f:Parentid'], t3['entityid']) 
    putdata(t3)
    
    t3=org_l1      
    t3['new_col'] = map(lambda x, y: do_something(x, y) , t3['f:Parentid'], t3['entityid']) 
    putdata(t3)
    
    
    
    for i in np.arange(ent_level_min,ent_level_max):
        
        count=i
        #只有level > 4级别的entity才能进入循环
        if i>4:
            
            jb=ent_l1[(ent_l1['I:Level']==np.str(count))]
            
            if i==5:
                jb=jb.ix[:,['f:EntityLnglat','I:Level','f:Parentid', 'entityid']]
                t1.append(jb)
            
            for j in np.arange(count,5,-1): 

                jb=transdata(jb,t) 
                #只有循环到最后一级别才能够append
                if j==6:                    
                    t1.append(jb)
    t3=[]
    for jj in np.arange(0,len(t1)):
        t2=t1[jj]        
        t2['new_col'] = map(lambda x, y: do_something(x, y) , t2['f:Parentid'], t2['entityid'])   
        putdata(t2)
        
        t3.append(t2)
    totalspenttime=time.time()-starttime   
    print("spent sencond %d"%totalspenttime)
    
