import numpy as np 
import pandas as pd 

from read_stock import READ_DATA
from com_b4_rght import adjust_price, complex_before_right
from indicators import INDICATOR
#from ml_model import train
from asset import ASSET
from backtest import BACKTEST
from common import record_error_msge
import os.path
if __name__ == "__main__":
    # set the directory of all the 5 minute bar files
    # and the full path of the panel data
    STOCK_LIST = [line.rstrip() for line in open('hushen_300_.txt')]
    TURN_DATE = pd.to_datetime('2016-01-01')
    CACHE_FILE = 'cache.txt'
    for stock in STOCK_LIST:
        print (stock)
        reader = READ_DATA(stock)
        print ("reading data...")
        df_finance = reader.read_finance()
        df_share = reader.read_share()
        if df_finance.empty or df_share.empty:
            #print ("No finance of share info of ", stock)
            record_error_msge(stock, 'No finance or share data')
            continue

        df_tech = reader.fast_read_tech()

        if df_tech is None:
            record_error_msge(stock, 'No tech data')
            continue
        df_panel = reader.read_panel()
        # complex before right
        print ("doing complex_before_right" )
        if df_panel.empty:
            record_error_msge(stock, 'No complex before right')
            pass
        else:
            df_tech = complex_before_right(df_tech, df_panel)
        # implement the indicators
        print ("implementing the indicators")
        indicator = INDICATOR(df_tech, df_finance, df_share)
        indicator.save_indicators(turnDate=TURN_DATE)
        if not os.path.isfile(CACHE_FILE):
            df_tech[df_tech.date>=TURN_DATE].reset_index(drop=True).to_csv(CACHE_FILE, index=None)
        else:
            with open(CACHE_FILE, 'a') as f:
                df_tech[df_tech.date>=TURN_DATE].reset_index(drop=True).to_csv(f, index=None, header=False)
        print ('recorded the data')


    #train the model
#    df_tech = train(df_tech)

    # get return of the strategy
    # first is measured by open
    # second is by close
 #   ass = ASSET(df_tech)
 #   print ("running the strategy")
 #   assetRecord, returnRecord = ass.make_order()

    # Do backtest then
 #   print ("doing backtest")
 #   test = BACKTEST(assetRecord)
 #   test.implement_backtest()


