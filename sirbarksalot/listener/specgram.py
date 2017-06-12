import numpy as np
import cv2
from scipy.io import wavfile
from matplotlib import mlab
import matplotlib.pyplot as plt

def preprocess(s):
    s = np.maximum(s, 10**(-10))
    return np.log10(s)

def create_spectrogram(data, n_fft=512, fs=44100, overlap=192, norm=False):
    params = {
        "NFFT": n_fft,
        "Fs": fs,
        "noverlap": overlap
    }
    _specgram, freqs, bins =  mlab.specgram(data.copy(), **params)
    _specgram = preprocess(_specgram)
    if norm:
        return min_max_scale(_specgram) / 255.
    return _specgram

def min_max_scale(img):
    _min, _max = np.min(img), np.max(img)
    return 255 * (img - _min) / (_max - _min)

def write_to_png(img, filename):
    out_image = np.zeros([img.shape[0], img.shape[1], 3])

    rescaled = min_max_scale(img).astype('Float32')

    out_image[:, :, 2] = rescaled
    cv2.imwrite(filename, out_image)


def save_specgram_to_file(data, filename, n_fft=512, fs=44100, overlap=192):
    """Spectrogram"""
    params = {
        "NFFT": n_fft,
        "Fs": fs,
        "noverlap": overlap
    }
    P, freqs, bins = mlab.specgram(data.copy(), **params)

    Z = np.log10(np.flipud(P))

    xextent = 0, np.amax(bins)
    xmin, xmax = xextent
    extent = xmin, xmax, freqs[0], freqs[-1]

    plt.figure(figsize=[20,6])
    im = plt.imshow(Z, extent=extent)
    plt.axis('auto')
    plt.xlim([0.0, bins[-1]])
    plt.ylim([0, 44100 / 2])
    plt.savefig(filename)
