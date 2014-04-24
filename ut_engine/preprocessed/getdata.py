#!/usr/bin/env python
# encoding: utf-8

import csv
reader=csv.reader(open('t_alibaba_data.csv'))
data=[]
reader.next()
for usrid,brandid,dtype,date in reader:
    datestr=date.decode('gb2312')
    print datestr
    splitdate=datestr.split(u'\u6708')
    print int(splitdate[0])
    data.append((usrid,brandid,dtype,date.decode('gb2312')))
    #break
print data[0]  #title info
print data[1]
#print data
#print reader[0]
import numpy as np
def formatdata(file='t_alibaba_data.csv'):
    data_list=[]
    reader=csv.reader(open(file))
    reader.next()
    for userid,brandid,type,date in reader:
        data_item=[]
        data_item.append(int(userid))
        data_item.append(int(brandid))
        data_item.append(int(type))
        data_item.append(int(date.decode('gb2312').split(u'\u6708')[0]))
        data_list.append(data_item)
    return np.array(data_list)

