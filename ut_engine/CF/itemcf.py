#!/usr/bin/env python
# encoding: utf-8

import math
import csv

from ut_engine.evaluate import evaluate


class ItemCF:
    def __init__(self,basefile,testfile):
        self.datafile=basefile
        self.testfile=testfile
        self.readData()
        self.readTestData()

    def readData(self):
        self.traindata={}
        reader=csv.reader(open(self.datafile))
        reader.next()
        for userid,brandid,dtype,date in reader:
            self.traindata.setdefault(userid,{})
            if dtype=='1':
                self.traindata[userid][brandid]=2
            elif dtype=='2':
                self.traindata[userid][brandid]=1
            else:
                self.traindata[userid][brandid]=int(dtype)
        #out put test
        ru=self.traindata.get("42000")
        print ru
        #print list
        file=open('output.txt','w')
        for id,iterms in sorted(self.traindata.items(),key=lambda x:x[0],reverse=False):
            print file,'%s,%s\n' %(id,iterms)

    def readTestData(self):
        self.testdata={}
        reader=csv.reader(open(self.testfile))
        reader.next()
        for userid,brandid,dtype,date in reader:
            #if dtype=='1' or True:
            self.testdata.setdefault(userid,{})
            self.testdata[userid][brandid]=int(dtype)

    def ItemSimilarity(self):
        train=self.traindata
        C=dict()
        N=dict()
        for u,items in train.items():
            for i in items.keys():
                N.setdefault(i,0)
                N[i]+=1
                for j in items.keys():
                    #if i=='14630':
                        #print 'this is in '
                        #print j

                    if i==j:
                        continue

                    C.setdefault(i,{})
                    C[i].setdefault(j,0)
                    C[i][j] += items[j]
        self.itemSimBest=dict()
        for i,related_items in C.items():
            self.itemSimBest.setdefault(i,{})
            for j,cij in related_items.items():
                self.itemSimBest[i].setdefault(j,0)
                self.itemSimBest[i][j]=cij/math.sqrt(N[i]*N[j])
    def Recommendation(self,userid,K=8,nitem=40):
        train=self.traindata
        rank=dict()
        ru=train.get(userid)
        for i,pi in ru.items():
#            print i,pi
#            print self.itemSimBest
            for j,wj in sorted(self.itemSimBest[i].items() if self.itemSimBest.has_key(i) else [],key=lambda x:x[1],reverse=True)[0:K]:
                if j in ru:
                    continue
                rank.setdefault(j,0)
                rank[j]+=pi*wj
        return dict(sorted(rank.items(),key=lambda x:x[1],reverse=True)[0:nitem])
    def recallAndPrecision(self,test=None,k=8,nitem=10):
        train=self.traindata
        test=self.testdata
        hit=0
        recall=0
        precision=0
        predictdata={}
        for user in train.keys():
            tu=test.get(user,{})
            #print tu
            rank=self.Recommendation(user,k,nitem)
            predictdata[user]=rank.keys()
            for item,_ in rank.items():
                if item in tu:
                    hit+=1
            recall+=len(tu)
            precision+=nitem
        evaluate.exportresult(predictdata)
        return (hit/(recall*1.0),hit/(precision*1.0))

def testItemCF():
    cf=ItemCF('t_alibaba_data.csv','test.csv')
    cf.ItemSimilarity()
    print "%5s%5s%20s%20s%20s" % ('K','N','recall','precision','F1-measure')
   # print cf.itemSimBest.keys()
    recall,precision=cf.recallAndPrecision(k=5,nitem=10)
   # for k in [5,10,20,40,80,160]:
   #     for nitem in [5,10,15,20]:
   #         recall,precision=cf.recallAndPrecision(k=k,nitem=nitem)
   #         f1measure=(2*precision*recall)/(precision+recall)
   #         print '%5d%5d%19.3f%%%19.3f%%%19.3f%%' %(k,nitem,recall*100,precision*100,f1measure*100)

if __name__=="__main__":
    testItemCF()

