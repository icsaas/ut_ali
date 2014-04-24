import numpy as np
def evaluate(predictdata,realdata):
    """predictdata: {'userid':['brandid1','brandid2',...]}
       realdata: {'userid':['brandid1','branid2',...]}
    """
    hitbrands=0
    pbrands=0
    bbrands=0
    for userid,brandids_p in predictdata.iteritems():
        brandids_r=realdata[userid] if realdata.has_key(userid) else []
        brandids_s=list(set(brandids_p) & set(brandids_r))
        hitbrands+=len(brandids_s)
        pbrands+=len(brandids_p)
        bbrands+=len(brandids_r)
    precision=float(hitbrands)/pbrands
    recall=float(hitbrands)/bbrands
    #print precision,recall
    f1measure=(2*precision*recall)/(precision+recall)
    print "%20s%20s%20s" % ('recall','precision','F1-measure')
    print '%19.3f%%%19.3f%%%19.3f%%' %(recall*100,precision*100,f1measure*100)
    return (precision,recall)

def score(precision,recall):
    f1=(2*precision*precision)/(precision+recall)
    return f1

def exportresult(predictdata):
    f=open('t_tmall_add_user_brand_predict_dh','w')
    for userid,brandids in predictdata.iteritems():
        line=str(userid)+" "
        brandstr=','.join(str(bid) for bid in brandids)
        line+=brandstr
        f.write(line)
        f.write('\n')

