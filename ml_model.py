from keras.models import Model, Sequential
from keras.layers import Input, Dense, Activation, Dropout
from keras.regularizers import l2, l1
import pandas as pd
import numpy as np
from sklearn import linear_model, preprocessing
from sklearn.metrics import classification_report

class ALGORITHM():
    def __init__(self):
        return

    def prepare_data(self, trainFname='cache/train.txt', testFname='cache/test.txt'):
        trainData = np.loadtxt(trainFname)
        testData = np.loadtxt(testFname)
        (X_train, Y_train) = (trainData[:, :-1], trainData[:, -1])
        (X_test, Y_test) = (testData[:, :-1], testData[:, -1])
        return (X_train, Y_train, X_test, Y_test)

    def preprocess_X(self, X):
        return preprocessing.scale(X)

    def preprocess_Y(self, Y):
        Y_ = np.zeros((len(Y), 3))
        msk1 = Y==0
        msk2 = Y==1
        msk3 = Y==2
        Y_[msk1, 0] = 1
        Y_[msk2, 1] = 1
        Y_[msk3, 2] = 1
        return Y_

    def train(self, X_train, Y_train, X_test, iter_):
        '''
        output: predicted class: 0, 1, 2
        '''
        inputs = Input(shape=(12,))
        x = Dense(48, activation='sigmoid', W_regularizer=l1(0.01))(inputs)
        drop = Dropout(0.2)(x)
        prediction = Dense(3, activation='sigmoid', W_regularizer=l1(0.01))(drop)
        model = Model(input=inputs, output=prediction)
        model.compile(optimizer='adagrad',
                      loss='poisson')
        model.fit(X_train, Y_train, nb_epoch=iter_, batch_size=100)
        pred = model.predict(X_test)
        return (np.argmax(pred, axis=1),
                np.max(pred, axis=1))

    def benchmark(self, X_train, Y_train, X_test):
        '''
        output: predicted class: -1, 0, 1
        '''
        lr = linear_model.LogisticRegression()
        model = lr.fit(X_train, Y_train)
        return (model.predict(X_test),
                np.max(model.predict_proba(X_test), axis=1))

    def evaluate(self, Y_pred, Y_true, method, fname='result.txt'):
        if method != 'NN' and method != 'LR':
            return ValueError('method just can be either NN or LR') 
        with open(fname, 'w+') as f:
            f.write(\
                    method\
                    + ':\n'\
                    + classification_report(Y_pred, Y_true)\
                    + '\n')
        msk = Y_pred == Y_true
        return msk.cumsum()[-1]/len(msk)

    def combine_to_df(self, class_, prob):
        return pd.DataFrame({'class_': class_, 'prob': prob})

    def run(self, iter_=100, folder='result/'):
        X_train, Y_train, X_test, Y_test = self.prepare_data()
        X_train_scale, X_test_scale = (self.preprocess_X(X_train), self.preprocess_X(X_test))
        Y_train_matrix, Y_test_matrix = (self.preprocess_Y(Y_train), self.preprocess_Y(Y_test))
        predNN = self.train(X_train_scale, Y_train_matrix, X_test_scale, iter_)
        predLR = self.benchmark(X_train_scale, Y_train, X_test_scale)
        self.combine_to_df(predNN[0], predNN[1])\
                                                .to_csv(folder+'predict_NN', index=False)
        self.combine_to_df(predLR[0], predLR[1])\
                                                .to_csv(folder+'predict_LR', index=False)

        accNN = self.evaluate(predNN[0], np.argmax(Y_test_matrix, axis=1), 'NN')
        accLR = self.evaluate(predLR[0], Y_test, 'LR')
        print ('NN accuracy: ', accNN)
        print ('LR accuracy: ', accLR)
        return 