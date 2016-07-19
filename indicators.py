import pandas as pd 
import numpy as np 
from common import scalify, lower_bound, select_val_b4_date, record_error_msge
from tempfile import TemporaryFile
import matplotlib.pyplot as plt

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
        self.M = 9
        self.N = 5
        self.U = 26
        self.df_y = df_y
        self.df_finance = df_finance
        self.df_share = df_share
        self.df_finance['average_asset_ratio_in_last_one_year'] = df_finance.apply(lambda row: np.average(df_finance.loc[row.name:row.name+4, p_asset_liability_ratio_].values), axis=1)
        self.df_finance['average_cash_ratio_in_last_one_year'] = df_finance.apply(lambda row: np.average(df_finance.loc[row.name:row.name+4, p_epcf_].values), axis=1)
        self.df_finance['eps_in_past_one_year'] = self.df_finance.apply(lambda row: self._get_eps_in_one_year(self.df_finance[row.name:row.name+5]), 1)
        self.id_ = scalify(self.df_y.stock_id.unique())

    def _slope_N_day(self, c0, cN, N):
        return ((c0 - cN) / cN) / N

    def _percentile_N_day(self, c0, H, L):
        return (c0 - L) / (H - L)

    def _ema(self, c_array):
        day = len(c_array)
        mul = 2 / (day + 1)
        if day == 1:
            return c_array.index[0]
        else:
            return (c_array.index[-1] - ema(c_array[:-1])) * mul + ema(c_array[:-1])

    def _price_oscillator(self, c_array, M=9, N=12):
        if M > len(c_array) or N > len(c_array):
            raise ValueError('M or N is bigger than the number of days')
        return (ema(c_array[-M:]) - ema(c_array[-N:])) / ema(c_array[-N:])

    def _recur_diff(self, array, result_array=None):
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

    def _volume_N_day(self, V, C):
        return np.sum(V * recur_diff(C)) 

    def _return_N_day(self, c0, cN):
        return (c0 - cN) / cN

    def _cal_ema(self, df, M):
        df = df.reset_index(drop=True)
        mul = 2 / (M + 1)
        ema = np.full(len(df), -np.inf)
        ema[0] = df.loc[0, 'close'] * mul
        for index in range(1, len(ema)):
            ema[index] = (df.loc[index, 'close'] - ema[index-1]) * mul + ema[index-1]
        return ema

    def construct_slope_N_day(self):
        return self.df_y.loc[self.N:].apply(lambda row: self._slope_N_day(row['close'], self.df_y.loc[row.name-self.N,'close'], self.N), axis=1)

    def construct_percentile_N_day(self):
        return self.df_y.loc[self.N:].apply(lambda row: self._percentile_N_day(row['close'],\
                                                        self.df_y.loc[row.name-self.N:row.name+1, 'high'].max(),\
                                                        self.df_y.loc[row.name-self.N:row.name+1, 'low'].min()\
                                            ), axis=1)

    def construct_return_N_day(self):
        return self.df_y.loc[self.N:].apply(lambda row: self._return_N_day(row.close, self.df_y.loc[row.name-self.N, 'close']), axis=1) 

    def construct_ema(self):
        emaM = self._cal_ema(self.df_y[self.N:], self.M)
        emaU = self._cal_ema(self.df_y[self.N:], self.U)
        print ('emaM: {0}; emaU: {1}'.format(np.shape(emaM), np.shape(emaU)))
        return (emaM - emaU) / emaU

    def pe_ratio(self):
        return self.df_y[self.N:].apply(lambda row: \
                                            scalify(\
                                                    row.close / \
                                                    select_val_b4_date(self.df_finance, row.date, 'eps_in_past_one_year')\
                                                    ), axis=1)
    
    def relative_pe_ratio(pe, avepe):
        return pe / avepe
    
    def pb_ratio(self):
        return self.df_y[self.N:].apply(lambda row: scalify(\
                                              self.df_finance[\
                                              (self.df_finance[p_date_]==lower_bound(self.df_finance, row.date))\
                                              &(~self.df_finance[p_bvps_].isnull())][p_bvps_].values\
                                              / row.close)

                                        , axis=1)
    
    def relative_pb_ratio(pb, avepb):
        return pb / avepb
    
    def current_cashflow_ratio(self):
        return self.df_y[self.N:].apply(lambda row: scalify(row.close / select_val_b4_date(self.df_finance, row.date, p_epcf_)), axis=1)
    
    def average_cashflow_ratio(self):
        return self.df_y[self.N:].apply(lambda row: scalify(row.close / select_val_b4_date(self.df_finance, row.date, 'average_cash_ratio_in_last_one_year')), axis=1)
    
    def current_debt_ratio(self):
        return self.df_y[self.N:].apply(lambda row: scalify(select_val_b4_date(self.df_finance, row.date, p_asset_liability_ratio_)), axis=1)

    def average_debt_ratio(self):
        return self.df_y[self.N:].apply(lambda row: scalify(select_val_b4_date(self.df_finance, row.date, 'average_asset_ratio_in_last_one_year')), axis=1)
    
    def market_capitalization(self):
        return self.df_y[self.N:].apply(lambda row: scalify(row.close * select_val_b4_date(self.df_share, row.date, p_equity_)), axis=1)
    
    def circulate_stock_value(self):
        return self.df_y[self.N:].apply(lambda row: scalify(row.close * select_val_b4_date(self.df_share, row.date, p_a_share_)), axis=1)

    def _eps_within_one_certain_year(self, arr):
        if len(arr) == 1:
            return arr
        elif len(arr) > 4:
            raise ValueError('Impossible that more than 4 rows in one year!')
        else:
            return arr[0] - arr[-1] 

    def _get_eps_in_one_year(self, df):
        df = df.reset_index(drop=True)
        if len(df) > 5:
            raise ValueError('Plese take the first five rows as input bitch')
        bLastYear = self._eps_within_one_certain_year(\
                                        df[df.year==np.min(df.year.values)][p_earn_per_share_].values)
        bThisYear = df[df.year==np.max(df.year.values)].loc[0, p_earn_per_share_]
        return scalify(bLastYear+bThisYear)

    def save_img(self, arr, fname, folder='graph/'):
        fig,ax = plt.subplots()  #create a new figure
        ax.plot(arr)
        fig.savefig(folder+fname)

    def implement_indicator(self):
        slopeNday = self.construct_slope_N_day()
        percentileNday = self.construct_percentile_N_day()
        returnNday = self.construct_return_N_day()
        #self.save_img(returnNday, self.id_+'_'+'returnNday.png')
        ema = self.construct_ema()
        pe = self.pe_ratio()
#        self.save_img(pe, self.id_+'_'+'pe.png')
        pb = self.pb_ratio()
#        self.save_img(pb, self.id_+'_'+'pb.png') 
        currCashRat = self.current_cashflow_ratio()
#        self.save_img(currCashRat, self.id_+'_'+'currCashRat.png')        
        aveCashRat =  self.average_cashflow_ratio()
        currDebtRat = self.current_debt_ratio()
        aveDebtRat =  self.average_debt_ratio()
        marketVal = self.market_capitalization()
        #self.save_img(marketVal, self.id_+'_'+'marketval.png')
        circuMarketVal = self.circulate_stock_value()
        #self.save_img(circuMarketVal, self.id_+'_'+'circulmarketval.png')
        return np.vstack((slopeNday, percentileNday, returnNday, ema, pe, pb, currCashRat, aveCashRat, currDebtRat, aveDebtRat, marketVal, circuMarketVal))
    
    def _tomorrow_trend(self, close1, close2, threshold=0):
        # close1: tomorrow
        # close2: today
        trend = (close1 - close2) / close2
        if trend > threshold:
            return 2
        elif -threshold < trend < threshold:
            return 1
        else:
            return 0
            
    def _get_trend(self):
        return self.df_y[self.N:-1].apply(lambda row: self._tomorrow_trend(self.df_y.loc[row.name+1, 'close'], row.close), axis=1).values

    def save_indicators(self, turnDate):
        # shape(output) should be num_data * (num_ind + 1)

        indicators = self.implement_indicator()
        
        # filter the null val       
        indicators = indicators[:, :-1]
        if np.isnan(indicators).any():
            print (
                    'THIS SON OF BITCH HAS NULL VAL',
                    self.id_)
            record_error_msge(self.id_, 'has null val')
            return

        trend = self._get_trend()
        trend = trend.reshape(len(trend), 1)
        print (np.shape(indicators))
        print (np.shape(trend))
        matrix = np.hstack((indicators.T, trend))

        msk = self.df_y[self.N:-1].date < turnDate
        if msk.all() or not msk.any():
            record_error_msge(self.id_, 'fail to split train and test')
            return 
        msk = msk.values
        (train, test) = (matrix[msk], matrix[~msk])
        assert train != test
        with open('train.txt', 'ab') as f1:            
            np.savetxt(f1, train)
        with open('test.txt', 'ab') as f2:
            np.savetxt(f2, test)
        with open('record.txt', 'a') as f3:
            f3.write(self.id_+'\t'+len(test)+'\n')
        return
