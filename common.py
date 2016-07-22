import numpy as np
import pandas as pd 

p_exchange_ = '交易所简称'
p_stock_id_ = '股票代码'
p_date_ = '时间'
p_earn_per_share_ = '每股收益(元)'
p_bvps_ = '每股净资产(元)'
p_roe_ = '净资产收益率(％)'
p_net_profit_ = '净利润(万元)'
p_npgr_ = '净利润增长率(%)'
p_wroe_ = '加权净资产收益率(%)'
p_asset_liability_ratio_ = '资产负债比率(%)'
p_cash_in_net_profit_ = '净利润现金含量(%)'
p_basic_earn_per_share_ = '基本每股收益(元)'
p_net_earn_per_share_ = '每股收益-扣除(元)'
p_dulute_earn_per_share_ = '每股收益-摊薄(元)'
p_capital_reserve_per_share_ = '每股资本公积金(元)'
p_udpps_ = '每股未分配利润(元)'
p_epcf_ = '每股经营现金流量(元)'
p_operating_net_cash_flow_ = '经营活动现金净流量增长率(%)'
p_equity_ = '总股本(亿股)'
p_limit_equity_ = '限售股份(亿股)'
p_a_share_ = '流通A股(亿股)'

def scalify(l):
    if type(l) != np.ndarray:
        return l
    elif len(l) > 1:
        raise ValueError('Not only one element!')  
    else:
        return l[0]

def lower_bound(df, dateCol, date):
    return np.max(df[df[dateCol]<date][dateCol])

def select_val_b4_date(df, date, dateCol, valCol):
    # default: the column of the date in the df is dateCol
    lb = np.max(df[df[dateCol]<=date][dateCol])
    return df[df[dateCol]==lb][valCol].values
    
def record_error_msge(id_, msge, fname='cache/errorLog.txt'):
    with open(fname, 'a') as f:
        f.write(id_+'\t'+msge+'\n')

def normalize_dict(dict_):
    sum_ = sum(list(dict_.values()))
    for k, v in dict_.items():
        dict_[k] = v / sum_
    return dict_