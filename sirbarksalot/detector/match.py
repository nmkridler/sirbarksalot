"""
"""

import numpy as np
import cv2
from scipy.io import wavfile
from ..listener.specgram import create_spectrogram

def get_simple_clip(filename):
    """"""
    _rate, _data = wavfile.read(filename)
    img = create_spectrogram(_data[:, 0])
    return img[:, 440:510].astype('Float32')

class MatchTemplate(object):
    def __init__(self, filename="../listener/test.wav"):
        self._template = get_simple_clip(filename)

    def calculate_score(self, img):
        mf = cv2.matchTemplate(img.astype('Float32'), self._template,
            cv2.TM_CCOEFF_NORMED)
        min_value, max_value, min_loc, max_loc = cv2.minMaxLoc(mf)
        return max_value
