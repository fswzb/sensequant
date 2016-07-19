import pandas as pd 
import numpy as np 
import common

class ASSET():
    """
        
    """ 

    def __init__(self, df, cash=100000, upThreshold=0.5, downThreshold=0.5):
        '''
            @df: stock_id, high, low, close, open, date, prob, class
        '''
        self.df.loc[1:, 'trend'] = df[1:].apply(lambda row: 1 if df.loc[row.name-1, 'close']<=14.3 else 0, axis=1)
        self.df = self.df[1:]
        self.df.loc[:, 'close'] = self.df.close.apply(lambda x: round(x, 2))
        self.df.loc[:, 'open'] = self.df.open.apply(lambda x: round(x, 2))
        self._cash = cash 
        self._share = 0

        self.df = df
        self.df_model = df_model
        self.WHOLE_PERIOD = whole_period 
        self.shareDict = shareDict
        self.assetRecord = np.array([self._new_measure_asset_val(\
                                                                 self.df[self.df.date==whole_period[0]], 
                                                                 self.shareDict,
                                                                 'open')])
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

    def _new_measure_asset_val(self, df, shareDict, type_):
        '''
            @df: same date
        '''
        if type_ != 'open' and type_ != 'close':
            raise ValueError ('open or close?')
        idList = list(shareDict.keys())
        priceList = [df[df.stock_id==id_, type_] for id_ in idList]
        priceArr = np.asarray(list(idList.values()))
        shareArr = np.asarray(list(shareDict.values()))
        return priceArr @ shareArr

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
        investVal = 0
        # sell 
        eachStockSell = asset * 0.1 / 30
        for stock in mostLikelyDown.iterrows():
            stock = stock[1]
            # check share 
            currShare = shareDict[stock.stock_id]
            share2sell = eachStockSell /\
                        (currShare * df[df.stock_id==stock.stock_id, 'open'])
            if share2sell <= shareDict[stock.stock_id]:
                investVal -= eachStockSell
                shareDict[stock.stock_id] -= share2sell
            else:
                investVal -= stock.open * shareDict[stock.stock_id] 
                shareDict[stock.stock_id] = 0 
        return (investVal, shareDict)

    def _buy_strategy(self, df, shareDict, cash, perc=0.1):
        df_up = df[df.class_==2]
        mostLikelyUp = self.choose_10_stock(df_up)
        for stock in mostLikelyUp.iterrows():
            stock = stock[1]
            investVal = 0
            # check if cash is enough
            invest2pay = 100 * df[df.stock_id==stock.stock_id, 'open']
            if cash > invest2pay:
                shareDict[stock.stock_id] += 100
                investVal += invest2pay
            else:
                continue
        return (investVal, shareDict)

    def new_make_order(self):
        for time in self.whole_period.iteritems():
            time = time[1]
            # measure the asset
            df = self.df[self.df.date==time]
            asset = self._new_measure_asset_val(df, self.shareDict, 'close')
            self.assetRecord = np.hstack((asset, self.assetRecord))
            # make order
            invest, self.shareDict = self._sell_strategy(df, self.shareDict, asset)
            self._cash -= invest
            invest, self.shareDict = self._buy_strategy(df, self.shareDict, self._cash)
            self._cash -= invest
        return self.assetRecord