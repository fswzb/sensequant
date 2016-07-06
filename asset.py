import pandas as pd 
import numpy as np 
<<<<<<< HEAD
import common

class ASSET():
    """
        
    """ 
    def __init__(self, df, cash=100000, upThreshold=0.5, downThreshold=0.5):
        self.df = df
        self.df_order = pd.DataFrame({'date': df[1:].date, \
                                      'prob': df[1:].apply(lambda row: row.up if row.up > row.down else row.down, axis=1), \
                                      'trend': df[1:].apply(lambda row: 1 if df.loc[row.name-1, 'close']<=14.3  else 0, axis=1)})
        self.df.loc[1:, 'trend'] = df[1:].apply(lambda row: 1 if df.loc[row.name-1, 'close']<=14.3  else 0, axis=1)
        self.df = self.df[1:]
        self.df.loc[:,'close'] = self.df.close.apply(lambda x: round(x, 2))
        self.df.loc[:,'open'] = self.df.open.apply(lambda x: round(x, 2))
        #df_order = df[(df.up>upThreshold)|(df.down>downThreshold)]
        #self.df_order = pd.DataFrame({'date': df_order.date, \
                                      #'prob': df_order.apply(lambda row: row.up if row.up > row.down else row.down, axis=1), \
                                      #'trend': df_order.apply(lambda row: 1 if row.up > row.down else 0, axis=1)})
=======

class ASSET(df):
    """

    """ 
    def __init__(self, df, df_order, cash=100, upThreshold=0.8, downThreshold=0.8):
        self.df = df
        df_order = df_order[(df_order.up>upThreshold)|(df_order.down>downThreshold)]
        self.df_order = pd.DataFrame({'date': df_order.date, \
                                'prob': df_order.apply(lambda row: row.up if row.up > row.down else row.down), \
                                'trend': df_order.apply(lambda row: 1 if row.up > row.down else 0)})
>>>>>>> 62850dfacbc7b830eef35675633a58e4ebf231c7
        self._cash = cash 
        self._share = 0
        #self.assetRecord = np.array([self._cash])

#    def _prob_to_invest(self):
#        prob = self.df_order.prob.values
        # $10 for 1 prob
#        invest = prob * 10
#        return invest
<<<<<<< HEAD

    def _strategy(self, row, price):
=======
    def _strategy(self, row):
>>>>>>> 62850dfacbc7b830eef35675633a58e4ebf231c7
        '''
            @row: trend, prob, date
        '''
        if row.trend == 1:
            # up
<<<<<<< HEAD
            invest = 100 * price
            if invest > self._cash:
                return(0, 0)
            share = common.scalify(invest/\
                                   self.df[self.df.date==row.date].open.values)
=======
            invest = 1 
            share = self.df[self.df.date==row.date].open /\
                    invest
>>>>>>> 62850dfacbc7b830eef35675633a58e4ebf231c7
            return (invest, share)
        
        elif row.trend == 0:
            # down
<<<<<<< HEAD
            if self._share == 0:
                return (0, 0)
            invest = -self._share * price
            share = common.scalify(invest/\
                                   self.df[self.df.date==row.date].open.values)
            return (invest, share)
            
        else:
            raise ValueError('No this kind of trend!')

    def _new_strategy(self, row, price):
        if row.trend == 1:
            invest = 100 * price
            if invest > self._cash:
                return (0, 0)
            share = invest/row.open
            return (invest, share)
        elif row.trend == 0:
            if self._share == 0:
                return (0, 0)
            invest = -self._share * price
            share = invest / price
            return (invest, share)
        else:
            pass

    def _measure_asset_val(self, lastOrderDate, todate):
=======
            invest = -1
            share = self.df[self.df.date==row.date].open /\
                    invest
            return (invest, share)
        
        else:
            raise ValueError('No this kind of trend!')

    def _measure_asset_val(lastOrderDate, todate):
>>>>>>> 62850dfacbc7b830eef35675633a58e4ebf231c7
        '''
            measure the value of each row:
            @pro, @begin_date, @end_date
        '''
        # TODO: fix the data type bug
<<<<<<< HEAD
        #(self.df[(lastOrderDate<self.df.date)])
        return self._cash + \
               self._share * \
               self.df[(self.df.date>=lastOrderDate)&(self.df.date<=todate)].open.values

    def _measure_return_val(self, lastOrderDate, todate):
        return self._cash + \
               self._share * \
               self.df[(self.df.date>=lastOrderDate)&(self.df.date<=todate)].close.values 
    
    def _new_measure_asset_val(self, val):
        return self._cash + self._share * val
=======
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
>>>>>>> 62850dfacbc7b830eef35675633a58e4ebf231c7

    def make_order(self):
        '''
            mark the cash during each order
            and the shares
        '''
<<<<<<< HEAD
        assetRecord = np.array([self._cash])
        returnRecord = np.array([self._cash])
        isFirstMeasure = True
        lastOrderDate = None
        for row in self.df_order.iterrows():
            row = row[1]
            invest, share = self._strategy(row, common.scalify(self.df[self.df.date==row.date].open.values))
            # 
=======
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
            
>>>>>>> 62850dfacbc7b830eef35675633a58e4ebf231c7
            if invest != 0:
                if self._share > 0:
                    # measure passed stock value
                    # and mark the asset 
<<<<<<< HEAD
                    print (self._measure_asset_val(lastOrderDate, row.date)[-1])
                    if isFirstMeasure:
                        assetRecord = np.hstack((assetRecord, \
                                                 self._measure_asset_val(lastOrderDate, row.date)))
                        returnRecord = np.hstack((returnRecord, \
                                                 self._measure_return_val(lastOrderDate, row.date)))
                        isFirstMeasure = False
                    else:
                        assetRecord = np.hstack((assetRecord[:-1], \
                                                 self._measure_asset_val(lastOrderDate, row.date)))
                        returnRecord = np.hstack((returnRecord[:-1], \
                                                  self._measure_return_val(lastOrderDate, row.date)))
                else:
                    pass
            else:
                print ('date:{3}, cash: {0}, overall_share: {1}， invest:{2}'.format(self._cash, self._share, invest, row.date))#print (invest, self._cash, share)
                continue
                
            #print (invest, self._cash, share)
            assert invest <= self._cash 
            assert -share <= self._share
            
            tax = 5 if np.absolute(invest) * 0.0003 < 5 else np.absolute(invest) * 0.0003
            self._cash = self._cash - (invest + tax) if invest != 0 else self._cash
            self._share += share
            print ('date: {3}, cash: {0}, overall_share: {1}， invest:{2}'.format(self._cash, self._share, invest, row.date))
            lastOrderDate = row.date
        assetRecord = np.hstack((assetRecord[:-1], \
                                 self._measure_asset_val(lastOrderDate, \
                                                         self.df_order.iloc[-1].date)))
        if isFirstMeasure:
            returnRecord = np.hstack((returnRecord, \
                                      self._measure_return_val(lastOrderDate, self.df_order.iloc[-1].date)))
        else:
            returnRecord = np.hstack((returnRecord[:-1], \
                                      self._measure_return_val(lastOrderDate, self.df_order.iloc[-1].date)))           
            

        return (assetRecord, returnRecord)
    
    def new_make_order(self):
        assetRecord = np.array([self._cash])
        returnRecord = np.array([self._cash])
        for row in self.df.iterrows():
            row = row[1]
            # measure the assert
            assetRecord = np.hstack((assetRecord, \
                                     self._new_measure_asset_val(\
                                                                 row.open)))
            # make order
            invest, share = self._new_strategy(row, row.open)
            assert invest <= self._cash 
            assert -share <= self._share
            tax = 5 if np.absolute(invest) * 0.0003 <= 5. else np.absolute(invest) * 0.0003
            self._cash = self._cash - (invest + tax) if invest != 0 else self._cash
            self._share += share
            asset = self._new_measure_asset_val(row.close)
            returnRecord = np.hstack((returnRecord, asset))
            #print ('date: {0}, asset:{1}, open:{5}, close:{4}, invest:{2}, share: {3}'.format(row.date, asset, invest, self._share, row.close, row.open))
        return (assetRecord, returnRecord)
    def measure_asset():
=======
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
>>>>>>> 62850dfacbc7b830eef35675633a58e4ebf231c7
        return