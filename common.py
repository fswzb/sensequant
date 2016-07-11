import numpy as np
import pandas as pd 

def scalify(l):
    if type(l) != np.ndarray:
        return l
    elif len(l) > 1:
        raise ValueError('Not only one element!')  
    else:
        return l[0]

def lower_bound(df, date):
    return  np.max(df[df[p_date_]<date][p_date_])

def select_val_b4_date(df, date, colname):
    # default: the column of the date in the df is p_date_
    lb = np.max(df[df[p_date_]<date][p_date_])
    return df[df[p_date_]==lb][colname].values
