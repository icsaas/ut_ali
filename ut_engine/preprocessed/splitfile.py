import csv
r=open('t_alibaba_data.csv')
reader=csv.reader(r)
reader.next()
testfile = open("testdemo.csv", "w")
for userid,brandid,record,rawdate in reader:
    date=rawdate.decode('gbk')
    ascdate=date.encode('ascii','ignore')
    print ascdate
    if ascdate.startswith('4'):
        linestr=[userid,brandid,record,rawdate]
        testfile.write(','.join(linestr))
        testfile.write('\n')
