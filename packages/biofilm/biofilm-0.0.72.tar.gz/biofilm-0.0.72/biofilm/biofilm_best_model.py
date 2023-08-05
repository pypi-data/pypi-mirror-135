from sklearn.neural_network import MLPClassifier as MLP
import dirtyopts
import dirtyopts as opts
import json
import biofilm.util.data as datautil
import numpy as np
import structout as so
from sklearn.metrics import  f1_score
import pprint



from sklearn.experimental import enable_hist_gradient_boosting

from sklearn.ensemble import HistGradientBoostingClassifier as HGB
optidoc='''
--out str jsongoeshere
--n_jobs int 1
'''
def optimize(X,Y,x,y, args):
    estim = HGB(early_stopping=  False,
    l2_regularization = 1.2274248991486793e-10,
    learning_rate =  0.021975317928366187,
    max_leaf_nodes =  152)

    estim.fit(X,Y)
    score = f1_score(y,estim.predict(x) )
    res = {'score': score}
    pprint.pprint(res)
    return res





def main():
    jdumpfile = lambda thing, filename:  open(filename,'w').write(json.dumps(thing))
    args = dirtyopts.parse(optidoc)
    data = datautil.getfold()
    res = optimize(*data,args)
    jdumpfile(res,args.out)

if __name__ == "__main__":
    main()



