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

class READ_DATA():
    def __init__(self, stockId):
        self.id_ = stockId

    def read_tech(self, path='/home/lcc/dataset/kline_5minute/sz/'):
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

    def fast_read_tech(self, path='/home/lcc/dataset/kline_5minute/data/'):
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

    def read_panel(self, fname='/home/lcc/dataset/stock_info'):
        df_panel = pd.read_csv(fname)
        df_panel = df_panel[(df_panel[p_stock_id]==self.id_)]
        df_panel[p_date] = pd.to_datetime(df_panel[p_date])
        return df_panel

    def read_finance(self, fname='/home/lcc/dataset/kline_5minute/stock_finance.txt'):
        df_finance = pd.read_csv(fname, dtype={p_stock_id_: str})
        df_finance = df_finance.drop('每股净资产(元).1', 1)
        df_finance = df_finance[df_finance[p_stock_id_]==self.id_].reset_index(drop=True)
        df_finance[p_date_] = pd.to_datetime(df_finance[p_date_])
        df_finance['year'] = df_finance[p_date_].apply(lambda time: time.year)
        df_finance['month'] = df_finance[p_date_].apply(lambda time: time.month)
        df_finance['day'] = df_finance[p_date_].apply(lambda time: time.day)
        return df_finance

    def read_share(self, fname='/home/lcc/dataset/kline_5minute/stock_share.txt'):
        df_share = pd.read_csv(fname, dtype={p_stock_id_: str})
        df_share = df_share[df_share[p_stock_id_]==self.id_]
        df_share[p_date_] = pd.to_datetime(df_share[p_date_])
        return df_share 