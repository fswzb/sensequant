import pandas as pd 
import numpy as np

from com_b4_rght import complex_before_right

df_tech = complex_before_right()

class indicator():

    def __init__():
        return
        
    def slope_N_day(c0, cN, N):
        return ((c0 - cN) / cN) / N

    def percentile_N_day(c0, L, H):
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

def get_x_value():
    x_1 = df_tech.loc[U:].apply(lambda row: slope_N_day(row['close'], df_tech.loc[row.name-N,'close'], N), axis=1)
    x_2 = df_tech.loc[U:].apply(lambda row: percentile_N_day(row['close'],\
                                                        df_tech.loc[row.name-N:row.name+1, 'high'].max(),\
                                                        df_tech.loc[row.name-N:row.name+1, 'low'].min()\
                                                        ), axis=1)
    x_3 = df_tech.loc[U:].apply(lambda row: price_oscillator(df_tech.loc[row.name-U:row.name+1, 'close']), axis=1)
    x_4 = df_tech.loc[U:].apply(lambda row: return_N_day(row.close, df_tech.loc[row.name-N, 'close']), axis=1)
    
    # #data * #indicator
    X = np.vstack((x_1, x_2, x_3, x_4)).T
    # TODO: scale the X  
    return X

def get_y_value():
    groups = df_tech.groupby(['stock_id', 'date'])
    col = ['stock_id', 'date', 'high', 'low', 'open', 'close']
    df_y = pd.DataFrame()
    for name, group in groups:
        if group.high.max() <= 0:
            continue
        stock_id = name[0]
        date = name[1]
        high = group.high.max()
        low = group[group['low']>0].low.min()
        open_ = group[(group['open'].astype(np.float))>0].iloc[0]['open']
        close = group.iloc[-1]['close']
        row = pd.Series([stock_id, date, high, low, open_, close])
        df_y = df_y.append(row, ignore_index=True)
    df_y.columns = col

    # up or not
    df_y['result'] = df_y.apply(lambda row: up_or_not(row['close'], row['open']), axis= 1)

    return df_y.result.value

