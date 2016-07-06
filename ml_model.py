import pandas as pd
import numpy as np

def train(df):
    groups = df.groupby(['stock_id', 'date'])
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
    return df_y