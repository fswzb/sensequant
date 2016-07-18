import numpy as np 
import pandas as pd 

if __name__ == '__main__':
    df4test = pd.read_csv('cache.txt')
    df4test = df4test.drop('index', axis=1)
    df_LR = pd.read_csv('predLR')
    df_NN = pd.read_csv('predNN')
    WHOLE_PERIOD = df_test.data.unique()

    