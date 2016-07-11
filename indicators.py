import pandas as pd 
import numpy as np 
from common import scalify, lower_bound, select_val_b4_date

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

class INDICATOR():
    def __init__(self, df_y, df_finance, df_share):
        self.df_y = df_y
        self.df_finance = df_finance
        self.df_share = df_share
        self.df_finance['average_asset_ratio_in_last_one_year'] = df_finance.apply(lambda row: np.average(df_finance.loc[row.name:row.name+4, p_asset_liability_ratio_].values), axis=1)
        self.df_finance['average_cash_ratio_in_last_one_year'] = df_finance.apply(lambda row: np.average(df_finance.loc[row.name:row.name+4, p_epcf_].values), axis=1)
        self.df_finance['eps_in_past_one_year'] = self._eps_within_one_certain_year()

    def slope_N_day(c0, cN, N):
        return ((c0 - cN) / cN) / N

    def percentile_N_day(c0, H, L):
        return (c0 - L) / (H - L)

    def ema(c_array):
        day = len(c_array)
        mul = 2 / (day + 1)
        if day == 1:
            return c_array.index[0]
        else:
            return (c_array.index[-1] - ema(c_array[:-1])) * mul + ema(c_array[:-1])

    def price_oscillator(c_array, M=9, N=12):
        if M > len(c_array) or N > len(c_array):
            raise ValueError('M or N is bigger than the number of days')
        return (ema(c_array[-M:]) - ema(c_array[-N:])) / ema(c_array[-N:])

    def recur_diff(array, result_array=None):
        l = len(array)
        if l > 1:
            diff = (array[0] - array[1]) / array[0]
            if result_array is None:
                result_array = np.array([diff])
            else:
                result_array = np.append(result_array, diff)
            return recur_diff(array[1:], result_array)
        else:
            return result_array

    def volume_N_day(V, C):
        return np.sum(V * recur_diff(C)) 

    def return_N_day(c0, cN):
        return (c0 - cN) / cN

    def pe_ratio(self):
        return self.df_y.apply(lambda row: \
                                            scalify(\
                                                    row.close / \
                                                    select_val_b4_date(self.df_finance, row.date, 'eps_in_past_one_year')\
                                                    ), axis=1)
    
    def relative_pe_ratio(pe, avepe):
        return pe / avepe
    
    def pb_ratio(self):
        return self.apply(lambda row: scalify(row.close \
                                            / self.df_finance[\
                                              (self.df_finance[p_date_]==lower_bound(self.df_finance, row.date))\
                                              &(~self.df_finance[p_bvps_].isnull())][p_bvps_].values)\
                         , axis=1)
    
    def relative_pb_ratio(pb, avepb):
        return pb / avepb
    
    def current_cashflow_ratio(self):
        return self.apply(lambda row: scalify(row.close / select_val_b4_date(self.df_finance, row.date, p_epcf_)), axis=1)
    
    def average_cashflow_ratio(self):
        return self.apply(lambda row: scalify(row.close / select_val_b4_date(self.df_finance, row.date, 'average_cash_ratio_in_last_one_year')), axis=1)
    
    def current_debt_ratio(self):
        return self.apply(lambda row: scalify(select_val_b4_date(self.df_finance, row.date, p_asset_liability_ratio_)), axis=1)

    def average_debt_ratio(self):
        return self.apply(lambda row: scalify(select_val_b4_date(self.df_finance, row.date, 'average_asset_ratio_in_last_one_year'])), axis=1)
    
    def market_capitalization(self):
        return self.apply(lambda row: scalify(row.close * select_val_b4_date(self.df_share, row.date, p_equity_)), axis=1)
    
    def circulate_stock_value(self):
        return self.apply(lambda row: scalify(row.close * select_val_b4_date(self.df_share, row.date, p_a_share_)), axis=1)

    def _eps_within_one_certain_year(self, arr):
        if len(arr) == 1:
            return arr
        elif len(arr) > 4:
            raise ValueError('Impossible that more than 4 rows in one year!')
        else:
            return arr[0] - arr[-1] 

    def _get_eps_in_one_year(self):
        self.df_finance = self.df_finance.reset_index(drop=True)
        if len(self.df_finance) > 5:
            raise ValueError('Plese take the first five rows as input bitch')
        bLastYear = self._eps_within_one_certain_year(\
                                        self.df_finance[self.df_finance.year==np.min(self.df_finance.year.values)][p_earn_per_share_].values)
        bThisYear = self.df_finance[self.df_finance.year==np.max(self.df_finance.year.values)].loc[0, p_earn_per_share_]
        return scalify(bLastYear+bThisYear)

    def implement_indicator(self):
        pe = self.pe_ratio()
        pb = self.pb_ratio()
        currCashRat = self.current_cashflow_ratio()
        aveCashRat =  self.average_cashflow_ratio()
        currDebtRat = self.current_debt_ratio()
        aveDebtRat =  self.average_debt_ratio()
        marketVal = self.market_capitalization()
        circuMarketVal = self.circulate_stock_value()
        