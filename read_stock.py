import pandas as pd 
import numpy as np

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

p_exchange_ = '交易所简称'
p_stock_id_ = '股票代码'
p_date_ = '时间'
p_earn_per_share_ = '每股收益(元)'
p_bvps_ = '每股净资产(元)'
p_roe_ = '净资产收益率(％)'
p_net_profit_ = '净利润(万元)'
p_npgr_ = '净利润增长率(%)'
p_wroe_ = '加权净资产收益率(%)'
p_asset_liability_ratio_ = '资产负债比率(%)'
p_cash_in_net_profit_ = '净利润现金含量(%)'
p_basic_earn_per_share_ = '基本每股收益(元)'
p_net_earn_per_share_ = '每股收益-扣除(元)'
p_dulute_earn_per_share_ = '每股收益-摊薄(元)'
p_capital_reserve_per_share_ = '每股资本公积金(元)'
p_udpps_ = '每股未分配利润(元)'
p_epcf_ = '每股经营现金流量(元)'
p_operating_net_cash_flow_ = '经营活动现金净流量增长率(%)'
p_equity_ = '总股本(亿股)'
p_limit_equity_ = '限售股份(亿股)'
p_a_share_ = '流通A股(亿股)'

STOCK_LIST = ['000011'] 

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

def read_finance(fname):
    df_finance = pd.read_csv(fname, dtype={p_stock_id_: str})
    df_finance = df_finance.drop('每股净资产(元).1', 1)
    #df_finance = df_finance[df_finance[p_stock_id_].isin(STOCK_LIST)].reset_index(drop=True)
    df_finance[p_date_] = pd.to_datetime(df_finance[p_date_])
    df_finance['year'] = df_finance[p_date_].apply(lambda time: time.year)
    df_finance['month'] = df_finance[p_date_].apply(lambda time: time.month)
    df_finance['day'] = df_finance[p_date_].apply(lambda time: time.day)
    return df_finance

def read_share(fname='/home/lcc/dataset/kline_5minute/stock_share.txt'):
    df_share = pd.read_csv(fname, dtype={p_stock_id_: str})
    df_share = df_share[df_share[p_stock_id_].isin(STOCK_LIST)]
