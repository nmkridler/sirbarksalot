
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

def baseline_model(input_shape=None):
	# create model
	model = Sequential()
	model.add(Conv2D(32, (5, 5), input_shape=input_shape, activation='relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.2))
	model.add(Flatten())
	model.add(Dense(64, activation='relu'))
	model.add(Dense(1, activation='softmax'))
	# Compile model
	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model

def pipeline(X, y, batch_size=32, epochs=20):
    """
    """
    enc = LabelEncoder()
    enc.fit(y)
    enc_y = enc.transform(y)
    # evaluate model with standardized dataset
    estimator = KerasClassifier(build_fn=baseline_model,
        nb_epoch=epochs, batch_size=batch_size, verbose=1,
        input_shape=X.shape[1:])
    kfold = StratifiedKFold(n_splits=4, shuffle=True, random_state=1337)
    results = cross_val_score(estimator, X, enc_y, cv=kfold)
    print "Results: {:.2f}% ({:.2f}%)".format(
        results.mean()*100, results.std()*100
        )
