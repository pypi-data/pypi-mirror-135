
def load(infile):
    import numpy as np
    d = np.load(infile)
    X,y = [d[f'arr_{x}'] for x in range(2)]
    return X,y

