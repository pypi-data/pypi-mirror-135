import numpy as np
from lmz import *
import os
import basics as ba
import re


# WE WANT TO CHANGE THIS TO LIST THE PARAMETERS OF GRADIENT DESCENT



from collections import defaultdict


def load2(folder,loader):
    res=[]
    ## if we have grad desc: add k[blabaa] to the defdict
    for f in os.listdir(folder): 
        a,fold,pp, bl = f.split("_")
        if a ==  "3":
            continue
        d=ba.jloadfile(folder+'/'+f)
        s = d['param']
        #ss = re.findall("'classifier:__choice__': '(\w+)'",s)[0]
        #if ss ==  'gradient_boosting':
        #print(f"{d['param']}")
        z = re.findall('classifier:(.+?),',s)
        res += z
    res.sort()
    return res


r = load2('./res5', ba.jloadfile)
import pprint
#pprint.pprint(r)
for e in r:
    print(e)
