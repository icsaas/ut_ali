#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys

def load_data(path):
    with file(path) as f:
        result = f.readlines()
    return result

def split(data, st, ed, output):
    with file(output, 'w') as f:
        for entry in data:
            month = int(entry.strip().split(',')[3])
            if st<=month and month<=ed:
                f.write(entry)

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print "usage: %s train_st train_ed test_st test_ed input_data" % sys.argv[0]
        exit(0)
    train_st = int(sys.argv[1])
    train_ed = int(sys.argv[2])
    test_st = int(sys.argv[3])
    test_ed = int(sys.argv[4])
    input_path = sys.argv[5]
    train_file = "train_%d_%d.csv" % (train_st, train_ed)
    test_file = "test_%d_%d.csv" % (test_st, test_ed)
    data = load_data(input_path)
    split(data, train_st, train_ed, train_file)
    split(data, test_st, test_ed, test_file)
