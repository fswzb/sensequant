import pandas as pd 
import numpy as np 

class INDICATOR():

    def __init__(df):
        self.df = df

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

    def eps_within_one_certain_year(arr):
        #print (arr)
        if len(arr) == 1:
            return arr
        elif len(arr) > 4:
            raise ValueError('Impossible that more than 4 column in one year!')
        else:
            return (arr[0] - arr[-1])
        
    def get_eps_in_one_year(df):
        if len(df) > 5:
            raise ValueError('Plese take the first five columns as input bitch')
        elif (df[p_earn_per_share_] == np.nan).any():
            return np.nan
        bLastYear = eps_within_one_certain_year(\
                                                df[df.year==np.min(df.year.values)][p_earn_per_share_].values)
        #print (bLastYear)
        bThisYear = eps_within_one_certain_year(\
                                                df[df.year==np.max(df.year.values)][p_earn_per_share_].values)
        #print (bThisYear)
        return scalify(bLastYear+bThisYear)

    