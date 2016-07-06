import numpy as np
import pandas as pd 


class BACKTEST():
    
    def __init__(self, assetArr, benchmark=False):
        # transform the asset array to return array
        self._assetArr = assetArr
        self.returnArr = np.diff(assetArr) / assetArr[:-1]

    def return_(self, mStart, mEnd):
        return (mEnd - mStart) / mStart

    def daily_return(self, P):
        diff = np.diff(P)
        return diff / P[:-1]

    def max_drawdown(self, P):
        diff = -np.diff(P) 
        return np.max(diff / P[:-1])

    def benchmark_annual_return(self, mStart, mEnd):
        return ((mEnd - mStart) / mStart)

    def annual_return(self, tr, n):
        return (1 + tr) ** (250 / n) - 1

    def algorithm_volatility(self, TR):
        return np.sqrt(np.var(TR) * 250)

    def benchmark_volatility():
        return

    def sharpe_ratio(self, tar, av, rfir=0.04):
        return (tar - rfir) / av

    def beta(self, TR, BR):
        return np.cov(TR, BR) / np.var(TR, BR)
        
    def alpha(self, tar, bar, beta, rfir=0.04):
        return tar - (beta * (bar - rfir) + rfir)

    def downside_risk(self, TAR, n):
        TAR_down = TAR[TAR < np.mean(TAR)]
        m = len(TAR_down)
        return np.sqrt(np.var(TAR_down, np.mean(TAR)) * 250)
        
    def sortino(self, tar, rfir, dr):
        return (tar - rfir) / dr
        
    def information_ratio(self, tar, bar, TR, BR):
        return (tar - bar) / np.std(TR - BR)

    # one stock
    def implement_backtest(self):

        totReturn = np.sum(self.returnArr)
        maxDrawdown = self.max_drawdown(self._assetArr)
        algoVola = self.algorithm_volatility(self.returnArr)
        totAnnReturn = self.annual_return(totReturn, len(self._assetArr))
        sharpeRat = self.sharpe_ratio(totAnnReturn, algoVola)
        print ("total return: {0}\nmax drawdown: {1}\nalgorithm volatility: {2}\nannualized return: {3}\nsharpe ratio: {4}"\
                .format(totReturn, maxDrawdown, algoVola, totAnnReturn, sharpeRat))