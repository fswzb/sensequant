import numpy as np 
import pandas as pd 

if __name__ == '__main__':
    df_test = pd.read_csv('cache.txt')
    df_test = df_test.drop('index', axis=1)
    WHOLE_PERIOD = df_test.data.unique()
    for time in WHOLE_PERIOD: