
import pandas as pd
import numpy as np

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D

from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import roc_curve, auc
from sklearn.linear_model import LogisticRegression

def baseline_model(input_shape=None):
    # create model
    model = Sequential()
    model.add(Conv2D(8, (5, 5), input_shape=input_shape, activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))
    model.add(Flatten())
    model.add(Dense(64, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    # Compile model
    model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    return model

def another_model(input_shape=None):
    model = Sequential()
    model.add(Conv2D(32, 5, 5, activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D())
    model.add(Conv2D(64, 3, 3, activation='relu'))
    model.add(MaxPooling2D())
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='Adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model

def recenter(x):
    print x.mean(), x.std()
    if x.std() == 0:
        return x
    return (x - x.mean()) / x.std()

def remove_nans_infs(x):
    isnan = np.isnan(x)
    isinf = np.isinf(x)
    x[isnan] = 0
    x[isinf] = 0
    return x

def run_folds(algo, X, y, folds):
    """
    """
    y_ = np.empty(y.size)
    _out = np.empty(y.size)
    for train, test in folds.split(X,y):
        print train.size, y[train].sum()
        algo.fit(X[train], y[train])
        y_[test] = algo.predict_proba(X[test])[:, 1]

        y_[test] = remove_nans_infs(y_[test])
        y_[test] = recenter(y_[test])
        _auc = calc_auc(y[test], y_[test])
        y_[test] = y_[test] + 0.5
        print "AUC: {:.4f}".format(_auc)

    return y_

def calc_auc(t, p):
    fpr, tpr, thresh = roc_curve(t, p)
    return auc(fpr, tpr)

def pipeline(X, y, batch_size=32, epochs=20, kfold=False, save=False):
    """
    """

    # evaluate model with standardized dataset
    if kfold:
        estimator = KerasClassifier(
        	build_fn=another_model,
            epochs=epochs,
        	batch_size=batch_size,
        	verbose=0,
            input_shape=X.shape[1:]
        )
        #
        kfold = StratifiedKFold(n_splits=4, shuffle=False, random_state=1337)
        _y = run_folds(estimator, X, y, kfold)
        _out = pd.DataFrame({
            "target": y,
            "prediction": _y
        })
        _out.to_csv("./cnnout.csv", index=False)

    if save:
        model = another_model(input_shape=X.shape[1:])
        model.fit(X, y, nb_epoch=epochs, batch_size=batch_size)
        model.save('./cnnmodel3.h5')
