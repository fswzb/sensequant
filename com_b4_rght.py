import pandas as pd 
import numpy as np

p_stock_id = '股票交易代码'
p_stock_title = '股票名称'
p_cash_divid_bt = '税前派现金额（人民币）（元）（1：X）'
p_date = '除权日'
p_cash_divid_at = '税后派现金额（人民币）（元）（1：X）'
p_stock_divid_rat = '送股比例（1：X）'
p_increa_trans_rat = '转增比例（1：X）'
p_reser_rat = '送转比例（1：X）'
p_allot_prc = '配股价格（元）'
p_allot_rat = '实际配股比例'

def adjust_price(price, cash_divid_at, reser_rat):
    return (price - float(cash_divid_at)) / (1 + float(reser_rat))

def complex_before_right(df_tech, df_panel):
    # set index
    df_tech = df_tech.reset_index(drop=False)
    #df_benchmark = df_tech[df_tech['stock_id']=='399300']  
    df_panel = df_panel[(df_panel[p_cash_divid_at]!='\\N') | (df_panel[p_cash_divid_at]!='\\N')]
    
    df = df_panel[[p_stock_id, p_cash_divid_bt, p_cash_divid_at, p_reser_rat, p_date]]
    for values in df.itertuples():
        stock_id = values[1]
        cash_divid_bt = values[2]
        cash_divid_at = values[3]
        reser_rat = values[4]
        date = values[5]
        if cash_divid_bt != '\\N':
            c = cash_divid_at
        elif cash_divid_at != '\\N':
            c = cash_divid_bt
        else:
            c = 0
        criteria = (df_tech['stock_id'] == stock_id) & (df_tech['date'] < date)
        df_tech.loc[criteria, ['high', 'low', 'open', 'close']] = df_tech[criteria][['high', 'low', 'open', 'close']].apply(adjust_price, args=(c, reser_rat,))

        return df_tech 

def in_day_unit(df_tech):
    groups = df_tech.groupby('date')
    col = ['stock_id', 'date', 'high', 'low', 'open', 'close']
    df_y = pd.DataFrame()
    for name, group in groups:
        if group.high.max() <= 0:
            continue
        stock_id = scalify(df_tech.stock_id[0])
        date = name
        high = group.high.max()
        low = group[group['low']>0].low.min()
        open_ = group[(group['open'].astype(np.float))>0].iloc[0]['open']
        close = group.iloc[-1]['close']
        row = pd.Series([stock_id, date, high, low, open_, close])
        df_y = df_y.append(row, ignore_index=True)
    df_y.columns = col     
    return df_y