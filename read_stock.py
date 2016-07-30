import pandas as pd 
import numpy as np
from common import scalify
from os import listdir
from os.path import isfile, join

class READ_DATA():
    def __init__(self, stockId):
        self.id_ = stockId

    def read_tech(self, path='/home/lcc/sensequant/kline_5minute/sz/'):
        files = [f for f in listdir(path) if isfile(join(path, f))]
        df_tech = None
        for f in files:
            date = f.split('.')[0]
            df = pd.read_csv(path+f, dtype={'stock_id': str})
            df = df[df['stock_id']==self.id_]
            df['date'] = date
            if df_tech is None:
                df_tech = df
            else:
                df_tech = pd.concat([df_tech, df])

        if df_tech.empty:
            return df_tech

        df_tech['date'] = pd.to_datetime(df_tech.date)
        #14000 => 14.000
        df_tech[['high', 'low', 'open', 'close']] = df_tech[['high', 'low', 'open', 'close']].apply(lambda x: x/1000)
        groups = df_tech.groupby(['stock_id', 'date'])
        col = ['stock_id', 'date', 'high', 'low', 'open', 'close']
        df_y = pd.DataFrame()
        for name, group in groups:
            if group.high.max() <= 0:
                continue
            stock_id = name[0]
            date = name[1]
            high = group.high.max()
            low = group[group['low']>0].low.min()
            open_ = group[(group['open'].astype(np.float))>0].iloc[0]['open']
            close = group.iloc[-1]['close']
            row = pd.Series([stock_id, date, high, low, open_, close])
            df_y = df_y.append(row, ignore_index=True)
        df_y.columns = col

        return df_y


    def read_hdf_of_one_stock(self, fname, dataset):
        df = pd.read_hdf(fname, dataset)
        df = df[df.stock_id==self.id_].reset_index(drop=True)
        df.date = pd.to_datetime(df.date)
        return df

    def fast_read_tech(self, path='/home/lcc/sensequant/kline_5minute/alldata/'):
        files = [f for f in listdir(path) if isfile(join(path, f))]
        df_tech = None
        for f in files:
            if f.split('.')[0] == self.id_:
                df_tech = pd.read_csv(path+f, dtype={'stock_id': str})
                df_tech['date'] = pd.to_datetime(df_tech.date, format='%Y%m%d')
                #14000 => 14.000
                df_tech[['high', 'low', 'open', 'close']] = df_tech[['high', 'low', 'open', 'close']].apply(lambda x: x/1000)
                groups = df_tech.groupby('date')
                col = ['stock_id', 'date', 'high', 'low', 'open', 'close']
                df_y = pd.DataFrame()
                for name, group in groups:
                    if group.high.max() <= 0:
                        continue
                    stock_id = self.id_
                    date = name
                    high = group.high.max()
                    low = group[group['low']>0].low.min()
                    open_ = group[(group['open'].astype(np.float))>0].iloc[0]['open']
                    close = group.iloc[-1]['close']
                    row = pd.Series([stock_id, date, high, low, open_, close])
                    df_y = df_y.append(row, ignore_index=True)
                df_y.columns = col 
            else:
                continue
        if df_tech is None:
            return df_tech
        else:
            return df_y               

    def read_panel(self, fname='/home/lcc/sensequant/kline_5minute/stock_info'):
        df_panel = pd.read_csv(fname)
        df_panel = df_panel[(df_panel[p_stock_id]==self.id_)]
        df_panel[p_date] = pd.to_datetime(df_panel[p_date])
        return df_panel

    def read_finance(self, fname='/home/lcc/sensequant/kline_5minute/stock_finance.txt'):
        df_finance = pd.read_csv(fname, dtype={p_stock_id_: str})
        df_finance = df_finance.drop('每股净资产(元).1', 1)
        df_finance = df_finance[df_finance[p_stock_id_]==self.id_].reset_index(drop=True)
        df_finance[p_date_] = pd.to_datetime(df_finance[p_date_])
        df_finance['year'] = df_finance[p_date_].apply(lambda time: time.year)
        df_finance['month'] = df_finance[p_date_].apply(lambda time: time.month)
        df_finance['day'] = df_finance[p_date_].apply(lambda time: time.day)
        return df_finance

    def read_share(self, fname='/home/lcc/sensequant/kline_5minute/stock_share.txt'):
        df_share = pd.read_csv(fname, dtype={p_stock_id_: str})
        df_share = df_share[df_share[p_stock_id_]==self.id_]
        df_share[p_date_] = pd.to_datetime(df_share[p_date_])
        return df_share 

    def read_dict(self, series, fname, symbol):
        dict_ = {}
        with open(fname) as f:
            for line in f:
                line = line.rstrip()
                line = line.split(symbol)
                if line[0] in series.values:
                    dict_[line[0]] = float(line[1])
                else: 
                    continue
        return dict_ 

    def read_dict_tem(self, series, fname, symbol):
        dict_ = {}
        with open(fname) as f:
            for line in f:
                line = line.rstrip()
                line = line.split(symbol)
                if line[0] in series.values:
                    dict_[line[0]] = float(scalify(line[1]))
                else: 
                    continue
        return dict_ 

