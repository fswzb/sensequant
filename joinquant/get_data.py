import pandas as pd
import numpy as np
import itertools
from src import configure
import sys 
# Add the Test Folder path to the sys.path list
sys.path.append('/home/lcc/sensequant/code')
# Now you can import your module
from src.com_b4_rght import  in_day_unit

class get_data():

    def __init__(self, fname):
        self.fname = configure.tech_hdf_file

    def history(self, start_date=None, end_date=None, count=None, filed='avg', stock_list=None):
        '''
        the resulting data frame is in a unit of day
        start_date OR count 
        '''
        def read_data(fname):
            df_all = pd.DataFrame()
            for stock in stock_list:
                df = pd.read_hdf(fname, stock)
                df = df.drop('index')
                df = in_day_unit(df)
                df_all = df_all.append(df)
            return df_all

        def open_(df):
            return df.loc[0, 'open']

        def close_(df):
            return df.iloc[-1]['close']

        def low(df):
            if count:
                return np.sort(df.low.values)[:count]

        def high(df):
            return np.sort(df.high.values)[-count:]

        def avg(df):
            return np.average(df[:count].close.values)

        def pre_close(df):
            return scalify(df[df.date==np.sort(df.date)[-count]].close.values)

        def integrate_into_df(series, colname):
            return pd.DataFrame(series, columns=[colname]).reset_index()
        
        if start_date and count:
            raise ValueError('CAN set count or start_date!')
        
        df_all = read_data(self.fname, stock_list)
        df_all = df_all[df_all.date > pd.to_datetime(start_date)] if start_date else df_all
        groups = df_all.groupby('stock_id')        
        
        if filed == 'open':
            result = groups.apply(open_)

        elif filed == 'low':
            result = groups.apply(close_)
        
        elif filed == 'high':
            result = groups.apply(high)

        elif filed == 'avg':
            result = groups.apply(ave)
        
        elif filed == 'pre_close':
            result = groups.apply(pre_close)
        else:
            raise ValueError('No such filed')

        return integrate_into_df(result, filed)

    def get_fundamentals(self, start_date, end_date, stock_id, colname_list):
        
        def has_same_element(l1, l2):
            for e in l1:
                if e in l2:
                    return True
            return False
        
        col4check = json.loads(open(configure.colnames_in_each_fundamental_df).read())
        msk = (df.date>=start_date)&(df.date<=end_date)&(df.stock_id==stock_id)
        result = pd.DataFrame()
        for df_name, columns in col4check.items():
            if has_same_element(stock_id, colname_list):
                df = pd.read_hdf(configure.fundamental_hdf_file, 
                                 df_name, 
                                 columns=columns_list+'stock_id'+'date', 
                                 where=['date>=pd.to_datetime(%s)' % start_date, 
                                        'date<=pd.to_datetime(%s)' % end_date,
                                        'stock_id==(%s)'% stock_id])
                if result.empty:
                    result = df
                else:
                    result = pd.merge(info, share, on=['stock_id', 'date'], how='outer')
        return result

    def get_fundamental_items(self):
        col4check = json.loads(open(configure.colnames_in_each_fundamental_df).read())
        for k,v in col4check.items():
            print ('%s: %s'(% k, % v))