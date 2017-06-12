
import pandas as pd
import numpy as np
from scipy.io import wavfile

from ..listener.specgram import create_spectrogram

from ..detector.match import MatchTemplate
_MT = MatchTemplate(filename="./sirbarksalot/listener/test.wav")
def get_corr_features(labels, target="is_bark", basedir=""):
    """
    """
    add_dir = lambda x: "{0}{1}".format(basedir, x)
    df = labels.assign(fpath=labels["filename"].apply(add_dir))
    kws = {"reshape": False, "downsample": False}
    data = [get_img(r.fpath, **kws) for i, r in df.iterrows()]

    # turn the images into correlation features
    scores = [_MT.calculate_score(d) for d in data]
    return np.array(scores).reshape((len(scores), 1)), labels[target].values

def get_labels(filename="labels.csv"):
    """ read the labels as a csv file

        this dataframe has columns
        filename, cody, caylee, alert, excited

            cody: cody is barking
            caylee: caylee is barking
            alert: bark is to alert that something happened
            excited: bark is due to excitement
    """
    df = pd.read_csv(filename)

    # create an is_bark column for any bark
    any_bark = lambda x: max(x["cody"], x["caylee"])
    df = df.assign(is_bark=df.apply(any_bark, axis=1))

    return df

DEFAULTS = {
    "n_fft": 512,
    "fs": 44100,
    "overlap": 192
}

def get_img(filename, parameters=DEFAULTS, reshape=True, downsample=True):
    """ create a single spectrogram
    """
    rate, data = wavfile.read(filename)
    img = create_spectrogram(data, norm=True, **parameters)
    if downsample:
        img = img[::4, ::16]
    if not reshape:
        return img
    n_pixels = img.shape[1] * img.shape[0]
    return img.reshape(img.shape + (1, ))

def get_spectrograms(labels, target="is_bark", basedir=""):
    """
    """
    add_dir = lambda x: "{0}{1}".format(basedir, x)
    df = labels.assign(fpath=labels["filename"].apply(add_dir))
    data = [get_img(r.fpath) for i, r in df.iterrows()]
    return np.array(data), labels[target].values
