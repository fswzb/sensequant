import numpy as np 
import pandas as pd 
from read_stock import READ_DATA
from ml_model import ALGORITHM

if __name__ == '__main__':
    df4test = pd.read_csv('cache.txt')
    df4test = df4test.drop('index', axis=1)
    algorithm = ALGORITHM()
    algorithm.run()
    
    predLR = pd.read_csv('predLR')
    predNN = pd.read_csv('predNN')
    # restore the abundant last day in the test file 
    lenRecord = pd.read_csv('record.txt', header=None, sep='\t', dtype={0:str})
    end = lenRecord[1].cumsum()
    start = np.hstack((0, end[:-1]))
    pd.DataFrame({'start': start})

    df_record = pd.concat([lenRecord, pd.DataFrame({'start': start})], axis=1, ignore_index=True)
    df_record = df_record.rename(columns={0: 'stock_id', 1: 'end', 2: 'start'})

    df4test['pred'] = np.nan
    df4test['class_'] = np.nan
    for row in df_record.iterrows():
        row = row[1]
        t = predNN[row.start: row.end]
        t = t.append({'prob': np.nan, 'class_': np.nan}, ignore_index=True)
        
        msk = df4test.stock_id==row.stock_id
        df4test.loc[msk, 'prob'] = t['prob'].values
        df4test.loc[msk, 'class_'] = t['class_'].values

    hs300_weight = READ_DATA.read_dict(fname='data/weight.txt', symbol=',')
