import numpy as np 
import pandas as pd 
from read_stock import READ_DATA

if __name__ == '__main__':
    df4test = pd.read_csv('cache.txt')
    df4test = df4test.drop('index', axis=1)
    predLR = pd.read_csv('predLR')
    predNN = pd.read_csv('predNN')
    # restore the abundant last day in the test file 
    lenRecord = pd.read_csv('record.txt', header=False)
    stockArr = lenRecord[0]
    end = lenRecord[1]
    start = np.hstack((0, end[:-1]))
    df_record = 

    df4test['pred'] = np.nan
    df4test['class_'] = np.nan
    for id_, df in df4test.groupby('stock_id'):

    #df4test = pd.concat([df4test, predNN], axis=0, ignore_index=False)
    hs300_weight = READ_DATA.read_dict(fname='data/weight.txt', symbol=',')



    