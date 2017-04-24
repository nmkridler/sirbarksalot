
from sirbarksalot.cnn.labels import get_spectrograms, get_labels
from sirbarksalot.cnn.train import pipeline
def main():
    df = get_labels("./labeled_clips/labels.csv")

    X, y = get_spectrograms(df, basedir="./labeled_clips/")
    print X.shape, y.shape

    params = {
        "batch_size": 16,
        "epochs": 200
    }
    pipeline(X, y, **params)


if __name__ == "__main__":
    main()
