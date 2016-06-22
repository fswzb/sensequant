import pandas as pd 
import numpy as np

from read_stock import read_tech, read_panel

def adjust_price(price, cash_divid_at, reser_rat):
    return (price - float(cash_divid_at)) / (1 + float(reser_rat))

def complex_before_right():
    df_tech = read_tech()
    # 14000 => 14.00
    df_tech[['high', 'low', 'open', 'close']] = df_tech[['high', 'low', 'open', 'close']].apply(lambda x: x/1000)
    # set index
    l = [n for n in range(len(df_tech))]
    df_tech = df_tech.set_index([l])

    df_benchmark = df_tech[df_tech['stock_id']=='399300']
    
    df_panel = read_panel()
    df_panel = df_panel[(df_panel[p_cash_divid_at]!='\\N') | (df_panel[p_cash_divid_at]!='\\N')]
    

    df = df_panel[[p_stock_id, p_cash_divid_at, p_reser_rat, p_date]]
    for values in df.itertuples():
        stock_id = values[1]
        cash_divid_at = values[2]
        reser_rat = values[3]
        #print (reser_rat)
        date = values[4]
        criteria = (df_tech['stock_id'] == stock_id) & (df_tech['date'] < date)
        df_tech.loc[criteria, ['high', 'low', 'open', 'close']] = df_tech[criteria][['high', 'low', 'open', 'close']].apply(adjust_price, args=(cash_divid_at, reser_rat,))

    return df_tech 