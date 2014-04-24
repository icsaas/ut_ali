import csv
from datetime import date
def format_file(raw_file='../../data/t_alibaba_data.csv',outputfile='../../data/user_brand_date_full1.csv'):
    r=open(raw_file)
    output=open(outputfile,'w')
    reader=csv.reader(r)
    reader.next()
    for userid,brandid,record,rawdate in reader:
        datestr=rawdate.decode('gb2312')
        splitdate=datestr.split(u'\u6708')
        month=splitdate[0]
        days=splitdate[1].split(u'\u65e5')
        day=days[0]
        items=[userid,brandid,record,month,day]
        line=','.join(items)
        output.write(line)
        output.write('\n')

if __name__=="__main__":
    format_file()
