from sklearn import linear_model, preprocessing
import pandas as pd 
import numpy as np

lr = linear_model.LogisticRegression(max_iter=200, class_weight="balanced")
X = np.vstack((x1, x2, x3, x4)).T
Y = df_y[U:].result.values
ratTrain = 0.6
msk = np.random.rand(len(Y)) < ratTrain
(Xtrain, Ytrain) = (X[msk], Y[msk])
(Xtest, Ytest) = (X[~msk], Y[~msk])
score = lr.fit(Xtrain, Ytrain).score(Xtest, Ytest)

print (score)