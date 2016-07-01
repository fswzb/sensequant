import pandas as pd 
import numpy as np 

class ASSET(df):
    """

    """ 
    def __init__(self, df, df_order, cash=100, upThreshold=0.8, downThreshold=0.8):
        self.df = df
        df_order = df_order[(df_order.up>upThreshold)|(df_order.down>downThreshold)]
        self.df_order = pd.DataFrame({'date': df_order.date, \
                                'prob': df_order.apply(lambda row: row.up if row.up > row.down else row.down), \
                                'trend': df_order.apply(lambda row: 1 if row.up > row.down else 0)})
        self._cash = cash 
        self._share = 0
        #self.assetRecord = np.array([self._cash])

#    def _prob_to_invest(self):
#        prob = self.df_order.prob.values
        # $10 for 1 prob
#        invest = prob * 10
#        return invest
    def _strategy(self, row):
        '''
            @row: trend, prob, date
        '''
        if row.trend == 1:
            # up
            invest = 1 
            share = self.df[self.df.date==row.date].open /\
                    invest
            return (invest, share)
        
        elif row.trend == 0:
            # down
            invest = -1
            share = self.df[self.df.date==row.date].open /\
                    invest
            return (invest, share)
        
        else:
            raise ValueError('No this kind of trend!')

    def _measure_asset_val(lastOrderDate, todate):
        '''
            measure the value of each row:
            @pro, @begin_date, @end_date
        '''
        # TODO: fix the data type bug
        '''
        return pd.Series(\
                        np.hstack(\
                        self.df[self.df.date==row.date].open.values,\
                        self.df[self.df.date==row.end_date].close.values]\
                        )\
                        )\
                        .values
        '''
        return self._cash + \
               self._share * \
               np.hstack((self.df[self.df.date==lastOrderDate].open.values, \
                          self.df[lastOrderDate<self.df.date<todate].close.values))

    def make_order(self):
        '''
            mark the cash during each order
            and the shares
        '''
#        invest = self._prob_to_invest()
        '''
        cashRecord = cash - invest.cumsum()
        
        if np.min(cashRecord) < 0:
            raise ValueError('NO MONEY!')
        
        share = invest / np.array(\
                        [\
                        group.loc[0, 'open'] \
                        for group in \
                        self.df[\
                        self.df.date.isin\
                        (self.df_order.begin_date)\
                        ]\
                        .groupby('date')\
                        ]\
                        )
        assert len(share) == len(cashRecord)
        return (cashRecord, share)
        '''
        assetRecord = np.array([self.cash])
        
        for row in self.df_order.iterrows():
            row = row[1]
            invest, share = self._strategy(row)
            
            if invest != 0:
                if self._share > 0:
                    # measure passed stock value
                    # and mark the asset 
                    assetRecord = np.hstack(assetRecord, \
                                            self._measure_asset_val(lastOrderDate, \
                                                                    row.date))
                    lastOrderDate = row.date
                else:
                    pass
            else:
                continue

            assert invest < self._cash and -share < self._share

            self._cash -= invest
            self._share += share

        assetRecord = np.hstack(assetRecord, \
                                     self._measure_asset_val(lastOrderDate, \
                                     self.df_order.iloc[-1].date))
        return assetRecord


    def measure_asset():
        '''
            @share: numpy array indicating the share of the stock for each hold
    
        
        cashRecord, share = self._make_order()
        asset = [] 
        for row in self.df_order.iterrows():
            idx = row[0]
            asset.append(share[idx] * _measure_stock_val(row[1]) + cashRecord[idx])

        return [cashRecord + stock for stock in stock_val]
        '''
        return