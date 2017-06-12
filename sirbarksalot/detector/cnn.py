

from keras.models import load_model
import numpy as np
import tensorflow as tf

class CNN(object):
    def __init__(self, filename="cnnmodel.h5"):
        self.model = load_model(filename)
        self.model.compile(loss='binary_crossentropy',
            optimizer='Adam', metrics=['accuracy'])
        self.graph = tf.get_default_graph()

    def calculate_score(self, img):
        # heavily downsample and reshape
        _img = img[::4, ::16]
        _img = _img.reshape((1,) + _img.shape + (1, ))
        with self.graph.as_default():
            predictions = self.model.predict_proba(_img)
            print predictions
        return predictions[0][0]
