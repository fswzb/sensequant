import numpy as np 
import pandas as pd 

from read_stock import read_tech, read_panel, read_finance, read_share
from com_b4_rght import adjust_price, complex_before_right
from indicators import INDICATOR
from ml_model import train
from asset import ASSET
from backtest import BACKTEST

if __name__ == "__main__":
	# set the directory of all the 5 minute bar files
	# and the full path of the panel data
	path = '/home/lcc/dataset/kline_5minute/sz/'
	fname = '/home/lcc/dataset/stock_info'
	print ("reading data...")
	df_tech =read_tech(path)
	df_panel = read_panel()
	df_finance = read_finance()
	df_share = read_share()

	# complex before right
	print ("doing complex_before_right" )
	df_tech = complex_before_right(df_tech, df_panel)

	# implement the indicators
	print ("implementing the indicators")
	indicator = INDICATOR(df_tech, df_finance, df_share)
	indicator.save_indicators()

	#train the model
	df_tech = train(df_tech)

	# get return of the strategy
	# first is measured by open
	# second is by close
	ass = ASSET(df_tech)
	print ("running the strategy")
	assetRecord, returnRecord = ass.make_order()

	# Do backtest then
	print ("doing backtest")
	test = BACKTEST(assetRecord)
	test.implement_backtest()


