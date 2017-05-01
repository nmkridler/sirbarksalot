import numpy as np
import cv2
from scipy.io import wavfile
from matplotlib import mlab

def preprocess(s):
    return np.log10(s)

def create_spectrogram(data, n_fft=512, fs=44100, overlap=192):
    params = {
        "NFFT": n_fft,
        "Fs": fs,
        "noverlap": overlap
    }
    _specgram, freqs, bins =  mlab.specgram(data.copy(), **params)
    # return preprocess(_specgram)
    return min_max_scale(_specgram) / 255.

def min_max_scale(img):
    _min, _max = np.min(img), np.max(img)
    return 255 * (img - _min) / (_max - _min)

def write_to_png(img, filename):
    out_image = np.zeros([img.shape[0], img.shape[1], 3])

    rescaled = min_max_scale(img).astype('Float32')

    out_image[:, :, 2] = rescaled
    cv2.imwrite(filename, out_image)
