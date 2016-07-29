import numpy as np 
import pandas as pd 
from read_stock import READ_DATA
from ml_model import ALGORITHM
from asset import ASSET
from common import normalize_dict
from backtest import BACKTEST
import matplotlib.pyplot as plt
import configure

CACHE_DIR = configure.cache_dir
CACHE_DF_FILE = CACHE_DIR + configure.cache_df_file 
PREDICT_NN_FILE = configure.result_dir + configure.result_NN_predict_file
PREDICT_LR_FILE = configure.result_dir + configure.result_LR_predict_file
RECORD_FILE = configure.cache_dir + configure.result_len_record
HUSHEN_300 = configure.hushen_300_weight
LAST_PRICE_FILE = configure.cache_dir+configure.cache_last_price_file

if __name__ == '__main__':
    folder = 'cache/'
    df4test = pd.read_csv(CACHE_DF_FILE, dtype={'stock_id': str})
    df4test = df4test.drop('index', axis=1)
    df4test.date = pd.to_datetime(df4test.date)
    algorithm = ALGORITHM()
    algorithm.run(iter_=500)
    
    predLR = pd.read_csv(PREDICT_LR_FILE)
    predNN = pd.read_csv(PREDICT_NN_FILE)
    # restore the abundant last day in the test file 
    lenRecord = pd.read_csv(RECORD_FILE, header=None, sep='\t', dtype={0:str})
    lenRecord[1] = lenRecord[1].cumsum()

    start = np.hstack((0, lenRecord[1][:-1]))

    df_record = pd.concat([lenRecord, pd.DataFrame({'start': start})], axis=1, ignore_index=True)
    df_record = df_record.rename(columns={0: 'stock_id', 1: 'end', 2: 'start'})

    df4test['prob'] = np.nan
    df4test['class_'] = np.nan
    for row in df_record.iterrows():
        row = row[1]
        t = predNN[row.start: row.end]
        t = t.append({'prob': np.nan, 'class_': np.nan}, ignore_index=True)
        
        msk = df4test.stock_id==row.stock_id
        df4test.loc[msk, 'prob'] = t['prob'].values
        df4test.loc[msk, 'class_'] = t['class_'].values

    reader = READ_DATA('000300')
    hs300_weight = reader.read_dict(df4test.stock_id, fname=HUSHEN_300, symbol=',')
    #hs300_weight = normalize_dict(hs300_weight)
    #print (sum(list(hs300_weight.values())))
    df_tem = reader.fast_read_tech()
    initPrice = reader.read_dict(df4test.stock_id, fname=LAST_PRICE_FILE, symbol='\t')
    #ass = ASSET(df_tem[df_tem.date>=pd.to_datetime('2016-01-01')], hs300_weight, initPrice)
    ass = ASSET(df4test, hs300_weight, initPrice)
    assetRecord = ass.new_make_order()

    fig,ax = plt.subplots()  #create a new figure
    ax.plot(assetRecord)
    fig.savefig('return')
    bt = BACKTEST(assetRecord)
    bt.implement_backtest()