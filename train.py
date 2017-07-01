
from sirbarksalot.cnn.labels import *
from sirbarksalot.cnn.train import pipeline



def main():
    df = get_labels("./labeled_clips/labels.csv")

    # X, y = get_corr_features(df, basedir="./labeled_clips/")
    X, y = get_spectrograms(df, basedir="./labeled_clips/")
    print X.shape, y.shape

    params = {
        "batch_size": 128,
        "epochs": 300,
        "save": True,
        "kfold": False
    }
    pipeline(X, y, **params)


if __name__ == "__main__":
    main()
