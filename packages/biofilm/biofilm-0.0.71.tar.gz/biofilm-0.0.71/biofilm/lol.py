import numpy as np
from lmz import *
import os
import basics as ba
import re


# READ THE RESULTS FILE

def load(folder,loader):
    r= []
    for f in os.listdir(folder): 
        a,fold,pp, bl = f.split("_")
        d=ba.jloadfile(folder+'/'+f)
        s = d['param']
        s = re.findall("'classifier:__choice__': '(\w+)'",s)[0]
        #print(f" {s}")
        res = [int(fold),pp,bl[:-5] , d['score'] ,s  ]
        r.append(res)
        
    return r 

from collections import defaultdict
def load2(folder,loader):

    deg = defaultdict(list)

    for f in os.listdir(folder): 
        a,fold,pp, bl = f.split("_")
        d=ba.jloadfile(folder+'/'+f)
        #s = d['param']
        #s = re.findall("'classifier:__choice__': '(\w+)'",s)[0]
        #print(f" {s}")
        fo,pp,bl,meth = [int(fold),pp,bl[:-5] , d['score']]
        deg[f"{bl}_{pp}"].append(meth)

    
    for k,v in list(deg.items()):
        deg[k] = np.mean(deg[k])

    return deg


r = load2('./res6', ba.jloadfile)
import pprint
pprint.pprint(r)
print(r)
