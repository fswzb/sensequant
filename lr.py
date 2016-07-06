from sklearn import linear_model, preprocessing
import pandas as pd 
import numpy as np

from get_x_y import get_x_value, get_y_value

lr = linear_model.LogisticRegression(max_iter=200, class_weight="balanced")
X = get_x_value()
Y = get_y_value()
ratTrain = 0.6
msk = np.random.rand(len(Y)) < ratTrain
(Xtrain, Ytrain) = (X[msk], Y[msk])
(Xtest, Ytest) = (X[~msk], Y[~msk])
score = lr.fit(Xtrain, Ytrain).score(Xtest, Ytest)

print (score)
