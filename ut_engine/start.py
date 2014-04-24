#/usr/bin/python
#-*- coding: utf-8 -*-

#system modules
import sys
#add root path into the sys.path
# sys.path.append('./')

#custom modules
from Model.model import Model
if __name__ == "__main__":
    if len(sys.argv)>1:
        cmd=sys.argv[1]
        if cmd=='score':
            from evaluate import score
            score.evaluator()
            exit(0)
        elif cmd=='result':
            print 'result'
            exit(0)
        elif cmd=='run':
            pass
        else:
            print "Usage: python start.py run|score|result"
            exit(0)

    #run the model
    betamodel=Model()
    betamodel.run()
