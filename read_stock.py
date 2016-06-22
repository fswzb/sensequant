import pandas as pd 
import numpy as np

from os import listdir
from os.path import isfile, join

p_stock_id = '股票交易代码'
p_stock_title = '股票名称'
p_cash_divid_pt = '税前派现金额（人民币）（元）（1：X）'
p_date = '除权日'
p_cash_divid_at = '税后派现金额（人民币）（元）（1：X）'
p_stock_divid_rat = '送股比例（1：X）'
p_increa_trans_rat = '转增比例（1：X）'
p_reser_rat = '送转比例（1：X）'
p_allot_prc = '配股价格（元）'
p_allot_rat = '实际配股比例'

STOCK_LIST = ['000002', '000099', '000004', '000005', '000006', '399300'] 

def read_tech(path = '/home/lcc/dataset/kline_5minute/sz/'):
    files = [f for f in listdir(path) if isfile(join(path, f))]
    df_tech = None
    for f in files:
        date = f.split('.')[0]
        df = pd.read_csv(path+f, dtype={'stock_id': str})
        df = df[df['stock_id'].isin(STOCK_LIST)]
        df['date'] = date
        if df_tech is None:
            df_tech = df
        else:
            df_tech = pd.concat([df_tech, df])
    df_tech['date'] = pd.to_datetime(df_tech.date)
    return df_tech

def read_panel(fname='/home/lcc/dataset/stock_info'):
    df_panel = pd.read_csv(fname)
    df_panel = df_panel[(df_panel[p_stock_id].isin(STOCK_LIST))]
    df_panel[p_date] = pd.to_datetime(df_panel[p_date])
    return df_panel

