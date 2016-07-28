import pandas as pd 
import numpy as np
#from sklearn import linear_model
#import seaborn as sns
#import matplotlib.pyplot as plt
#from sklearn import preprocessing
from itertools import groupby
from os import listdir
from os.path import isfile, join

p_stock_id = '股票交易代码'
p_stock_title = '股票名称'
p_cash_divid_bt = '税前派现金额（人民币）（元）（1：X）'
p_date = '除权日'
p_cash_divid_at = '税后派现金额（人民币）（元）（1：X）'
p_stock_divid_rat = '送股比例（1：X）'
p_increa_trans_rat = '转增比例（1：X）'
p_reser_rat = '送转比例（1：X）'
p_allot_prc = '配股价格（元）'
p_allot_rat = '实际配股比例'

def adjust_price(price, cash_divid_at, reser_rat):
    return (price - float(cash_divid_at)) / (1 + float(reser_rat))

def complex_before_right(df_tech, df_panel):
    # set index
    df_tech = df_tech.reset_index(drop=False)
    #df_benchmark = df_tech[df_tech['stock_id']=='399300']  
    df_panel = df_panel[(df_panel[p_cash_divid_at]!='\\N') | (df_panel[p_cash_divid_at]!='\\N')]
    
    df = df_panel[[p_stock_id, p_cash_divid_bt, p_cash_divid_at, p_reser_rat, p_date]]
    for values in df.itertuples():
        stock_id = values[1]
        cash_divid_bt = values[2]
        cash_divid_at = values[3]
        reser_rat = values[4]
        date = values[5]
        if cash_divid_bt != '\\N':
            c = cash_divid_at
        elif cash_divid_at != '\\N':
            c = cash_divid_bt
        else:
            c = 0
        criteria = (df_tech['stock_id'] == stock_id) & (df_tech['date'] < date)
        df_tech.loc[criteria, ['high', 'low', 'open', 'close']] = df_tech[criteria][['high', 'low', 'open', 'close']].apply(adjust_price, args=(c, reser_rat,))

        return df_tech 

def read_panel(id_, fname='/home/lcc/sensequant/kline_5minute/stock_info'):
    df_panel = pd.read_csv(fname)
    df_panel = df_panel[(df_panel[p_stock_id]==id_)]
    df_panel[p_date] = pd.to_datetime(df_panel[p_date])
    return df_panel

def read_finance(fname='/home/lcc/sensequant/kline_5minute/stock_finance.txt'):
    df_finance = pd.read_csv(fname, dtype={p_stock_id_: str})
    df_finance = df_finance.drop('每股净资产(元).1', 1)
    df_finance = df_finance[df_finance[p_stock_id_]==id_].reset_index(drop=True)
    df_finance[p_date_] = pd.to_datetime(df_finance[p_date_])
    df_finance['year'] = df_finance[p_date_].apply(lambda time: time.year)
    df_finance['month'] = df_finance[p_date_].apply(lambda time: time.month)
    df_finance['day'] = df_finance[p_date_].apply(lambda time: time.day)
    return df_finance

def read_share(fname='/home/lcc/sensequant/kline_5minute/stock_share.txt'):
    df_share = pd.read_csv(fname, dtype={p_stock_id_: str})
    df_share = df_share[df_share[p_stock_id_]==id_]
    df_share[p_date_] = pd.to_datetime(df_share[p_date_])
    return df_share 

if __name__ == '__main__':
    path = '/home/lcc/sensequant/kline_5minute/alldata/'
    file = [f for f in listdir(path) if isfile(join(path, f))]
    for f in file:
        df_tech = pd.read_csv(path+f, dtype={'stock_id': str})
        df_tech['date'] = pd.to_datetime(df_tech.date, format='%Y%m%d')
        df_tech[['high', 'low', 'open', 'close']] = df_tech[['high', 'low', 'open', 'close']].apply(lambda x: x/1000)
        df_panel = read_panel(f.split('.')[0])
        if df_panel.empty:
            pass
        else:
            df_tech = complex_before_right(df_tech, df_panel)
        df_tech.to_hdf('after_com.h5', f.split('.')[0])