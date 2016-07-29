import numpy as np
import pandas as pd 
import configure

ERROR_FILE = configure.cache_dir + configure.cache_record_error_msge_file

def scalify(l):
    if type(l) != np.ndarray:
        return l
    elif len(l) > 1:
        raise ValueError('Not only one element!')  
    else:
        return l[0]

def lower_bound(df, date, dateCol):
    return np.max(df[df[dateCol]<date][dateCol])

def select_val_b4_date(df, date, dateCol, valCol):
    # default: the column of the date in the df is dateCol
    lb = np.max(df[df[dateCol]<=date][dateCol])
    return df[df[dateCol]==lb][valCol].values
    
def record_error_msge(id_, msge, fname=ERROR_FILE):
    with open(fname, 'a') as f:
        f.write(id_+'\t'+msge+'\n')

def normalize_dict(dict_):
    sum_ = sum(list(dict_.values()))
    for k, v in dict_.items():
        dict_[k] = v / sum_
    return dict_