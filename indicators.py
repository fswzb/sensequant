import pandas as pd 
import numpy as np 
from common import scalify, lower_bound, select_val_b4_date, record_error_msge
from tempfile import TemporaryFile
import matplotlib.pyplot as plt

class INDICATOR():
    def __init__(self, df_y, df_finance, df_share):
        self.M = 9
        self.N = 5
        self.U = 26
        self.df_y = df_y
        self.df_finance = df_finance
        self.df_share = df_share
        self.df_finance['average_asset_ratio_in_last_one_year'] = df_finance.apply(lambda row: np.average(df_finance.loc[row.name:row.name+4, 'asset_liability_rat'].values), axis=1)
        self.df_finance['average_cash_ratio_in_last_one_year'] = df_finance.apply(lambda row: np.average(df_finance.loc[row.name:row.name+4, 'cash_flow_per_share'].values), axis=1)
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
        # TODO: if all the price are the same in N days
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
                                                    select_val_b4_date(self.df_finance, row.date, 'date', 'eps_in_past_one_year')/\
                                                    row.close\
                                                    ), axis=1)
    
    def relative_pe_ratio(pe, avepe):
        return pe / avepe
    
    def pb_ratio(self):
        return self.df_y[self.N:].apply(lambda row:  row.close/\
                                                     scalify(\
                                                           self.df_finance[\
                                                           (self.df_finance['date']==lower_bound(self.df_finance, row.date, 'date'))\
                                                           &(~self.df_finance['net_asset_per_share'].isnull())]['net_asset_per_share'].values\
                                                            )

                                        , axis=1)
    
    def relative_pb_ratio(pb, avepb):
        return pb / avepb
    
    def current_cashflow_ratio(self):
        return self.df_y[self.N:].apply(lambda row: scalify(row.close / select_val_b4_date(self.df_finance, row.date, 'date', 'cash_flow_per_share')), axis=1)
    
    def average_cashflow_ratio(self):
        return self.df_y[self.N:].apply(lambda row: scalify(row.close / select_val_b4_date(self.df_finance, row.date, 'date', 'average_cash_ratio_in_last_one_year')), axis=1)
    
    def current_debt_ratio(self):
        return self.df_y[self.N:].apply(lambda row: scalify(select_val_b4_date(self.df_finance, row.date, 'date', 'asset_liability_rat')), axis=1)

    def average_debt_ratio(self):
        # TODO: if the debt is null
        return self.df_y[self.N:].apply(lambda row: scalify(select_val_b4_date(self.df_finance, row.date, 'date', 'average_asset_ratio_in_last_one_year')), axis=1)
    
    def market_capitalization(self):
        return self.df_y[self.N:].apply(lambda row: scalify(row.close * select_val_b4_date(self.df_share, row.date, 'date', 'total_equity')), axis=1)
    
    def circulate_stock_value(self):
        return self.df_y[self.N:].apply(lambda row: scalify(row.close * select_val_b4_date(self.df_share, row.date, 'date', 'circulate_share')), axis=1)

    def _eps_within_one_certain_year(self, arr):
        if len(arr) == 1:
            return arr
        elif len(arr) > 4:
            raise ValueError('Impossible that more than 4 rows in one year!')
        else:
            return arr[0] - arr[-1] 

    def _get_eps_in_one_year(self, df):
        # TODO: if there a na in the eps in past year
        df = df.reset_index(drop=True)
        if len(df) > 5:
            raise ValueError('Plese take the first five rows as input bitch')
        bLastYear = self._eps_within_one_certain_year(\
                                        df[df.year==np.min(df.year.values)]['eps'].values)
        bThisYear = df[df.year==np.max(df.year.values)].loc[0, 'eps']
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
        self.save_img(pe, self.id_+'_'+'pe.png')
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
        return np.vstack((slopeNday, 
                          percentileNday, 
                          returnNday, 
                          ema, 
                          pe, 
                          pb, 
                          currCashRat, 
                          aveCashRat, 
                          currDebtRat, 
                          aveDebtRat, 
                          marketVal, 
                          circuMarketVal))
    
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

    def save_indicators(self, turnDate, folder):
        # shape(output) should be num_data * (num_ind + 1)

        indicators = self.implement_indicator()
        
        # filter the null val       
        indicators = indicators[:, :-1]
        if np.isnan(indicators).any():
            record_error_msge(self.id_, 'has null val')
            return False

        trend = self._get_trend()
        trend = trend.reshape(len(trend), 1)
        print (np.shape(indicators))
        print (np.shape(trend))
        matrix = np.hstack((indicators.T, trend))
        print (np.max(self.df_y.date))
        msk = self.df_y[self.N:-1].date < turnDate
        if msk.all() or not msk.any():
            record_error_msge(self.id_, 'fail to split train and test')
            return False
        msk = msk.values
        (train, test) = (matrix[msk], matrix[~msk])
        assert train != test
        with open(folder+'train.txt', 'ab') as f1:            
            np.savetxt(f1, train)
        with open(folder+'test.txt', 'ab') as f2:
            np.savetxt(f2, test)
        with open(folder+'record.txt', 'a') as f3:
            f3.write(self.id_+'\t'+str(len(test))+'\n')
        return True
