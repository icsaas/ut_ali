#!/usr/bin/env python
# encoding: utf-8

import csv
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

