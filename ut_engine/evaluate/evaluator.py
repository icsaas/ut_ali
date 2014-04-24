#!/usr/bin/python
#-*- coding: utf-8 -*-
import sys
from collections import defaultdict as ddict

def load_test(path):
    test = ddict(list)
    with file(path) as f:
        for line in f:
            elements = line.strip().split(',')
            if elements[2] != '1': continue
            uid = int(elements[0])
            bid = int(elements[1])
            test[uid].append(bid)
    return test

def load_predict(path):
    predict = ddict(list)
    with file(path) as f:
        for line in f:
            elements = line.strip().split(' ')
            uid = int(elements[0])
            predict[uid] = map(lambda x: int(x), elements[1].split(','))
    return predict

def evaluate(test, predict):
    hitBrand = 0
    pBrand = 0
    for uid in predict:
        pBrand += len(predict[uid])
        hitBrand += len(set(predict[uid]) & set(test[uid]))
    P = 1.0*hitBrand/pBrand

    hitBrand = 0
    bBrand = 0
    for uid in test:
        bBrand += len(test[uid])
        hitBrand += len(set(predict[uid]) & set(test[uid]))
    R = 1.0*hitBrand/bBrand

    F1 = 2*P*R/(P+R)
    print "F1=%f\nP=%f\nR=%f\n" % (F1, P, R)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: %s test_data predict_data\n" % sys.argv[0]
        exit(0)
    test = load_test(sys.argv[1])
    predict = load_predict(sys.argv[2])
    evaluate(test, predict)
