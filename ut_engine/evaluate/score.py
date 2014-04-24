#!/usr/bin/env python
# encoding: utf-8
import evaluate
def evaluator(predictfile='../output/latest/result.txt',realfile='../data/test.csv'):
    r=open(predictfile)
    predictdata={}
    for line in r:
        userid,brandids=line.split()
        predictdata[userid]=brandids.split(',')

    import csv
    reader=csv.reader(open(realfile))
    reader.next()
    testdata={}
    for userid,brandid,dtype,date in reader:
        if dtype=='1':
            brandids=testdata[userid] if testdata.has_key(userid) else []
            if brandid not in brandids:
                brandids.append(brandid)
            testdata[userid]=brandids

    evaluate.evaluate(predictdata,testdata)

