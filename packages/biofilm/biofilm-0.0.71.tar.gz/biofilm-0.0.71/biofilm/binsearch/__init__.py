from biofilm.binsearch import binsearch



import numpy as np
import structout as so

def optimize(f,a,b,rounds=3, debug = False):
    d={}
    for i in range(3):
        ran =np.linspace(a,b,10)
        valz = [f(x) for x in ran]
        srt =ran[np.argmax(valz)]
        dis = ran[1] - ran[0]
        #d.update(dict(zip(ran,valz)))
        a,b = srt-dis, srt +dis
        if debug:
            so.lprint(valz)
            print(f"opti",a,b, valz)
    return srt,d
        




