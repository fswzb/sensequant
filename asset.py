import pandas as pd 
import numpy as np 
from common import scalify, lower_bound, select_val_b4_date

class ASSET():
    """
        
    """ 

    def __init__(self, df, shareDict, initPrice, upThreshold=0.5, downThreshold=0.5):
        '''
            @df: stock_id, high, low, close, open, date, prob, class
        '''

        self._cash = 0
        self.df = df
        self.df.loc[:, 'close'] = self.df.close.apply(lambda x: round(x, 2))
        self.df.loc[:, 'open'] = self.df.open.apply(lambda x: round(x, 2))
        self.shareDict = self._get_init_share(shareDict)
        self.sDate = np.min(self.df.date)
        self.initPrice = initPrice
        self.assetRecord = np.array([])

    def _get_init_share(self, shareDict):
        min_ = min(list(shareDict.values()))
        for k, v in shareDict.items():
            shareDict[k] = int(v * 100 / min_)
        return shareDict

    def choose_10_stock(self, df, n=10):
        '''
            @df: same mode 
        '''
        msk = df.prob.isin(\
                            df.prob.sort(ascending=False, inplace=False).head(n))
        return df[msk]

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

    def _new_measure_asset_val(self, df, date, shareDict, cash, type_):
        '''
            @df: same date
        '''
        print (date)
        if type_ != 'open' and type_ != 'close':
            raise ValueError ('open or close?')
        sum_ = 0
        for id_, share in shareDict.items():
            if id_ in df.stock_id:
                sum_ += share *\
                        scalify(select_val_b4_date(self.df[self.df.stock_id==id_], date, 'date', type_))
            else:
                sum_ += share * self.initPrice[id_]
        sum_ += cash
        return sum_

    def _sell_strategy(self, df, shareDict, asset, perc=0.1):
        # choose 10 most likely to down
        # sell
        # choose 10 most likely to up
        # iterate and buy
        '''
            @df: same date
        '''
        df_down = df[df.class_==0]

        mostLikelyDown = self.choose_10_stock(df_down)
        num_ = len(mostLikelyDown)
        if num_ == 0:
            return (0, shareDict)
        invest = 0
        # sell 
        eachStockSell = asset * 0.01 / num_
        for stock in mostLikelyDown.iterrows():
            stock = stock[1]
            # check share 
            share2sell = scalify(eachStockSell / stock.open)
            if share2sell <= shareDict[stock.stock_id]:
                invest -= eachStockSell
                shareDict[stock.stock_id] -= share2sell
            else:
                invest -= stock.open * shareDict[stock.stock_id] 
                shareDict[stock.stock_id] = 0 
        return (invest, shareDict)

    def _buy_strategy(self, df, shareDict, budget, perc=0.1):
        df_up = df[df.class_==2]
        mostLikelyUp = self.choose_10_stock(df_up)
        invest = 0
        for stock in mostLikelyUp.iterrows():
            stock = stock[1]
            # check if budget is enough
            invest2pay = 100 * stock.open
            if budget >= invest2pay:
                shareDict[stock.stock_id] += 100
                invest += invest2pay
                budget -= invest2pay
            else:
                continue
        return (invest, shareDict)

    def new_make_order(self):
        for date, df in self.df.groupby('date'):
            # measure the asset
            asset = self._new_measure_asset_val(df, date, self.shareDict, self._cash, 'open')
            self.assetRecord = np.hstack((asset, self.assetRecord))
            # make order
            invest, self.shareDict = self._sell_strategy(df, self.shareDict, asset)
            self._cash -= invest
            invest, self.shareDict = self._buy_strategy(df, self.shareDict, self._cash)
            self._cash -= invest
            assert self._cash >= 0
            assert (np.array(list(self.shareDict.values())) >= 0).all()
        return self.assetRecord