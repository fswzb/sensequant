<<<<<<< HEAD
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
=======
def BACKTEST(assetArr, benchmark=False):
    def __init__():
        # transform the asset array to return array
        self.assetArr = assetArr
        self.returnArr = np.diff(assetArr) / assetArr[:-1]


    def return_(mStart, mEnd):
        return (mEnd - mStart) / mStart

    def daily_return(P):
        diff = np.diff(P)
        return diff / P[:-1]

    def max_drawdown(P):
        diff = -np.diff(P) 
        return np.max(diff / P[:-1])

    def benchmark_annual_return(mStart, mEnd):
        return ((mEnd - mStart) / mStart)

    def annual_return(tr, n):
        return (1 + tr) ** (250 / n) - 1

    def algorithm_volatility(TR):
>>>>>>> 62850dfacbc7b830eef35675633a58e4ebf231c7
        return np.sqrt(np.var(TR) * 250)

    def benchmark_volatility():
        return

<<<<<<< HEAD
    def sharpe_ratio(self, tar, av, rfir=0.04):
        return (tar - rfir) / av

    def beta(self, TR, BR):
        return np.cov(TR, BR) / np.var(TR, BR)
        
    def alpha(self, tar, bar, beta, rfir=0.04):
        return tar - (beta * (bar - rfir) + rfir)

    def downside_risk(self, TAR, n):
=======
    def sharpe_ratio(tar, av, rfir=0.04):
        return (tar - rfir) / av

    def beta(TR, BR):
        return np.cov(TR, BR) / np.var(TR, BR)
        
    def alpha(tar, bar, beta, rfir=0.04):
        return tar - (beta * (bar - rfir) + rfir)

    def downside_risk(TAR, n):
>>>>>>> 62850dfacbc7b830eef35675633a58e4ebf231c7
        TAR_down = TAR[TAR < np.mean(TAR)]
        m = len(TAR_down)
        return np.sqrt(np.var(TAR_down, np.mean(TAR)) * 250)
        
<<<<<<< HEAD
    def sortino(self, tar, rfir, dr):
        return (tar - rfir) / dr
        
    def information_ratio(self, tar, bar, TR, BR):
=======
    def sortino(tar, rfir, dr):
        return (tar - rfir) / dr
        
    def information_ratio(tar, bar, TR, BR):
>>>>>>> 62850dfacbc7b830eef35675633a58e4ebf231c7
        return (tar - bar) / np.std(TR - BR)

    # one stock
    def implement_backtest(self):

        totReturn = np.sum(self.returnArr)
<<<<<<< HEAD
        maxDrawdown = self.max_drawdown(self._assetArr)
        algoVola = self.algorithm_volatility(self.returnArr)
        totAnnReturn = self.annual_return(totReturn, len(self._assetArr))
        sharpeRat = self.sharpe_ratio(totAnnReturn, algoVola)
        print ("total return: {0}\nmax drawdown: {1}\nalgorithm volatility: {2}\nannualized return: {3}\nsharpe ratio: {4}"\
                .format(totReturn, maxDrawdown, algoVola, totAnnReturn, sharpeRat))
=======
        maxDrawdown = max_drawdown(self.assetArr)
        algoVola = algorithm_volatility(self.returnArr, len(returnArr))
        totAnnReturn = annual_return(totReturn)
        sharpeRat = sharpe_ratio(totAnnReturn, algoVola)
        # for maxdrawdown, 
        '''
        for idxSlice in orderIdx:
            closeArr = df.loc[idxSlice, 'close'].values
            print (closeArr)
            drawdown = max_drawdown(closeArr)
            maxDrawdown = drawdown if maxDrawdown < drawdown else maxDrawdown
            # daily_return
            totDayReturn = np.append(totDayReturn, daily_return(closeArr))
            # return
            totReturn += return_(closeArr[0], closeArr[-1])
        if benchmark:
            print ('benchmark return: '+totReturn)
            return 0
        # measure algorithm_volatility, annual_return, shape_ratio
        algoVola = algorithm_volatility(totDayReturn)
        n = len(totDayReturn)
        totAnnReturn = annual_return(totReturn, n)
        orders = np.hstack(orderIdx)
        closeArr = df.loc[orders, 'close'].values
        sharpeRat = sharpe_ratio(totAnnReturn, algoVola)
        '''
        print ("total return: {0}\nmax drawdown: {1}\nalgorithm volatility: {2}\nannualized return: {3}\nsharpe ratio: {4}"\
                .format(totReturn, maxDrawdown, algoVola, totAnnReturn, sharpeRat))
        return 0
>>>>>>> 62850dfacbc7b830eef35675633a58e4ebf231c7
