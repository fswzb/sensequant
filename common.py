def scalify(l):
    if type(l) != np.ndarray:
        return l
    elif len(l) > 1:
        raise ValueError('Not only one element!')  
    else:
        return l[0]
