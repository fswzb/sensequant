from keras.models import Model, Sequential
from keras.layers import Input, Dense, Activation, Dropout
from keras.regularizers import l2
import pandas as pd
import numpy as np
from sklearn import linear_model, preprocessing
from sklearn.metrics import classification_report

class ALGORITHM():
    def __init__(self):
        return

    def prepare_data(self, trainFname='train.txt', testFname='test.txt'):
        trainData = np.loadtxt('train.txt')
        testData = np.loadtxt('test.txt')
        (X_train, Y_train) = (trainData[:, :-1], trainData[:, -1])
        (X_test, Y_test) = (testData[:, :-1], testData[:, -1])
        return (X_train, Y_train, X_test, Y_test)

    def preprocess_X(self, X):
        return preprocessing.scale(X)

    def preprocess_Y(self, Y):
        Y_ = np.zeros((len(Y), 3))
        msk1 = Y==-1
        msk2 = Y==0
        msk3 = Y==1
        Y_[msk1, 0] = 1
        Y_[msk2, 1] = 1
        Y_[msk3, 2] = 1
        return Y_

    def train(self, X_train, Y_train):
        inputs = Input(shape=(12,))
        x = Dense(24, activation='relu', W_regularizer=l2(0.01))(inputs)
        drop = Dropout(0.2)(x)
        prediction = Dense(3, activation='softmax', W_regularizer=l2(0.01))(drop)
        model = Model(input=inputs, output=prediction)
        model.compile(optimizer='adadelta',
                      loss='categorical_crossentropy')
        model.fit(X_train, Y_train, nb_epoch=1000)
        return np.argmax(model.predict(X_test), axis=1)

    def benchmark(self, X_train, Y_train, X_test):
        lr = linear_model.LogisticRegression()
        return lr.fit(X_train, Y_train).predict(X_test)

    def evaluate(self, Y_pred, Y_true, method, fname='result.txt'):
        if method != 'NN' and method != 'LR':
            return ValueError('method just can be either NN or LR') 
        with open(fname, 'w+') as f:
            f.write(\
                    method\
                    + ':\n'\
                    + classification_report(Y_pred, Y_true)
                    + '\n')

        return 
 
    def run(self):
        X_train, Y_train, X_test, Y_test = self.prepare_data()
        X_train_scale, X_test_scale = (self.preprocess_X(X_train), self.preprocess_X(X_test))
        Y_train_matrix = self.preprocess_Y(Y_train)
        predNN = self.train(X_train_scale, Y_train_matrix)
        predLR = self.benchmark(X_train_scale, Y_train, X_test_scale)
        self.evaluate(predNN, Y_test, 'NN')
        self.evaluate(predLR, Y_test, 'LR')
        return