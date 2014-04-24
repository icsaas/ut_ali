#!/usr/bin/env python
# encoding: utf-8

import csv

from ut_engine.evaluate import evaluate

reader=csv.reader(open('train.csv'))
def parse_date(raw_date):
    entry_date = raw_date.decode("gbk")
    month = int(entry_date[0])
    if len(entry_date) == 5:
        day = 10 * int(entry_date[2]) + int(entry_date[3])
    else:
        day = int(entry_date[2])
    return 2013, month, day
from datetime import date
def split_file(raw_file, seperate_day, begin_date):
    train = open("train.csv", "w")
    validation = open("validation.csv", "w")
    raw_file.readline()
    for line in raw_file.readlines():
        line = line.strip()
        entry = line.split(",")
        entry_date = date(*parse_date(entry[3]))
        date_delta = (entry_date - begin_date).days
        if date_delta < seperate_day:
            train.write(",".join(entry[:3]) + "," + str(date_delta) + "\n")
        elif int(entry[2]) == 1:
            validation.write(",".join(entry[:2]) + "\n")
            print ",".join(entry[:2])
    validation.write("99999999999,9" + "\n")
    train.close()
    validation.close()

def generate_result(validation):
    entrys = validation.readlines()
    entrys.sort(key=lambda x: x.split(",")[0])
    result = open("result.txt", "w")
    for index, entry in enumerate(entrys):
        uid, tid = entry.strip().split(",")
        if index == 0:
            cur_id = uid
            cur_result = [tid]
        elif uid == cur_id:
            cur_result.append(tid)
        else:
            result.write(cur_id + "\t" + ",".join(set(cur_result)) + "\n")
            cur_id = uid
            cur_result = [tid]
    result.close()

SEPERATEDAY = date(2013, 7, 15)
BEGINDAY = date(2013, 4, 15)
raw_file = open("t_alibaba_data.csv")
split_file(raw_file, (SEPERATEDAY - BEGINDAY).days, BEGINDAY)
raw_file.close()
validation = open("validation.csv")
generate_result(validation)


#data=[]
#reader.next()
#predictdata={}
#i=1
#for usrid,brandid,dtype,date in reader:
    #if i==10000:
     #   break
#    datestr=date.decode('gb2312')
#    print datestr
#    splitdate=datestr.split(u'\u6708')
#    print int(splitdate[0])
#    i+=1
#    data.append((usrid,brandid,dtype,date.decode('gb2312')))
#    brandids=predictdata[usrid] if predictdata.has_key(usrid) else {}
#    brandids.setdefault(brandid,0)
#    if dtype=='0':
#        dtype=1
#    elif dtype=='1':
#        dtype=3
#    elif dtype=='2':
#        dtype=2
#    elif dtype=='3':
#        dtype=4
#    brandids[brandid]+=int(dtype)
#    predictdata[usrid]=brandids
#for usrid,brandids in predictdata.items():
#    brand_array=sorted(brandids.iteritems(),key=lambda d:d[1],reverse=True)
#    brandid_list=[item[0] for item in brand_array]
#    predictdata[usrid]=brandid_list[:6] if len(brandid_list)>6 else brandid_list
    #if dtype=='3':
    #    if brandid not in brandids:
    #        brandids.append(brandid)
    #    predictdata[usrid]=brandids
r=open('result.txt')
predictdata={}
for line in r:
    userid,brandids=line.split()
    predictdata[userid]=brandids.split(',')

reader=csv.reader(open('test.csv'))
reader.next()
testdata={}
for userid,brandid,dtype,date in reader:
    if dtype=='1':
        brandids=testdata[userid] if testdata.has_key(userid) else []
        if brandid not in brandids:
            brandids.append(brandid)
        testdata[userid]=brandids
evaluate.evaluate(predictdata,testdata)


