import numpy as np 
import matplotlib.pyplot as plt 
from scipy.io import wavfile 
from matplotlib import mlab 

def create_spectrogram(data, n_fft=512, fs=44100, overlap=192):
    params = {
        "NFFT": n_fft,
        "Fs": fs,
        "noverlap": overlap
    }
    return mlab.specgram(data, **params)

def write_to_png(P, filename):
    fig = plt.figure()
    plt.imshow(np.log10(np.flipud(P)))
    plt.axis('off')
    fig.savefig(filename, bbox_inches=0)
