import numpy as np 
import pandas as pd 
from read_stock import READ_DATA
from ml_model import ALGORITHM
from asset import ASSET
from common import normalize_dict
from backtest import BACKTEST
import matplotlib.pyplot as plt

if __name__ == '__main__':
    folder = 'cache/'
    df4test = pd.read_csv(folder+'cache.txt', dtype={'stock_id': str})
    df4test = df4test.drop('index', axis=1)
    df4test.date = pd.to_datetime(df4test.date)
    algorithm = ALGORITHM()
    algorithm.run(iter_=1000)
    
    predLR = pd.read_csv('result/predict_LR')
    predNN = pd.read_csv('result/predict_NN')
    # restore the abundant last day in the test file 
    lenRecord = pd.read_csv(folder+'record.txt', header=None, sep='\t', dtype={0:str})
    lenRecord[1] = lenRecord[1].cumsum()

    start = np.hstack((0, lenRecord[1][:-1]))

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

    reader = READ_DATA('000001')
    hs300_weight = reader.read_dict(df4test.stock_id, fname='data/weight.txt', symbol=',')
    hs300_weight = normalize_dict(hs300_weight)

    initPrice = reader.read_dict(df4test.stock_id, fname='cache/last_price.txt', symbol='\t')
    ass = ASSET(df4test, hs300_weight, initPrice)
    assetRecord = ass.new_make_order()

    fig,ax = plt.subplots()  #create a new figure
    ax.plot(assetRecord)
    fig.savefig('return')

    bt = BACKTEST(assetRecord)
    bt.implement_backtest()