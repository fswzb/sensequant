import pandas as pd 
import numpy as np 
import common

class ASSET():
    """
        
    """ 
    def __init__(self, df, cash=100000, upThreshold=0.5, downThreshold=0.5):
        self.df = df
        self.df.loc[1:, 'trend'] = df[1:].apply(lambda row: 1 if df.loc[row.name-1, 'close']<=14.3 else 0, axis=1)
        self.df = self.df[1:]
        self.df.loc[:, 'close'] = self.df.close.apply(lambda x: round(x, 2))
        self.df.loc[:, 'open'] = self.df.open.apply(lambda x: round(x, 2))
        self._cash = cash 
        self._share = 0

    def _strategy(self, row, price):
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
    
    def _measure_asset_val(self, price):
        return self._cash + self._share * price
    
    def make_order(self):
        assetRecord = np.array([self._cash])
        returnRecord = np.array([self._cash])
        for row in self.df.iterrows():
            row = row[1]
            # measure the assert
            assetRecord = np.hstack((assetRecord, \
                                     self._measure_asset_val(row.open)))
            # make order
            invest, share = self._strategy(row, row.open)
            assert invest <= self._cash 
            assert -share <= self._share
            tax = 5 if np.absolute(invest) * 0.0003 <= 5. else np.absolute(invest) * 0.0003
            self._cash = self._cash - (invest + tax) if invest != 0 else self._cash
            self._share += share
            returnRecord = np.hstack((returnRecord, \
                                      self._measure_asset_val(row.close)))
        return (assetRecord, returnRecord)