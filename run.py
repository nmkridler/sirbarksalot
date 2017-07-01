from sirbarksalot.lib.scheduler import Scheduler
from sirbarksalot.listener.listen import Listener
from sirbarksalot.listener.specgram import create_spectrogram, write_to_png
from sirbarksalot.listener.specgram import save_specgram_to_file, min_max_scale
from sirbarksalot.detector.match import MatchTemplate
from sirbarksalot.detector.cnn import CNN
from sirbarksalot.messenger.facebook import URL, create_app
import os
PHONE_NUMBER = os.environ["PHONE_NUMBER"]


import cv2
import time
def make_filename(ext, ms):
    return "./clips/sample_{0}.{1}".format(ms, ext)

import requests
import logging
logging.basicConfig()
logger = logging.getLogger("sirbarksalot")
logger.setLevel('INFO')

_MT = MatchTemplate(filename="./sirbarksalot/listener/test.wav")
_CNN = CNN(filename="cnnmodel3.h5")

_LISTEN = Listener()
_LISTEN.start_stream()
def send_message(corr, count):
    msg = {'text': 'woof woof: {:.4f}'.format(corr)}
    if count > 1:
        msg['text'] = '{0:d} woofs: {1:.4f}'.format(count, corr)

    payload = {
        'recipient': {'phone_number': PHONE_NUMBER},
        'message': msg
    }

    headers = {'Content-Type': 'application/json'}
    r = requests.post(URL, json=payload, headers=headers)
    print r

def listen():

    # get some data
    data = _LISTEN.record()

    # make a spectrogram
    _specgram = create_spectrogram(data)
    scoreMT = _MT.calculate_score(_specgram)
    scoreCNN = _CNN.calculate_score(min_max_scale(_specgram) / 255.)
    _MT.counter += 1

    # write it out
    if (scoreMT > 0.75) or (scoreCNN > 0.75):
        _ms = "{0}".format(time.time()).split(".")[0]
        logger.info("{0}|{1}|{2}".format(_ms, scoreMT, scoreCNN))
        if scoreMT > 0.75:
            _MT.save_score(scoreMT)

        _LISTEN.write_to_file(data, make_filename("wav", _ms))
        save_specgram_to_file(data, make_filename("png", _ms))

    if _MT.counter == 10:
        if _MT.scores:
            send_message(_MT.mean(), len(_MT.scores))

        _MT.reset_scores()
        _MT.counter = 0
    return 0


app = create_app()

if __name__ == "__main__":
    scheduler = Scheduler(6, listen)
    scheduler.start()
    app.run(debug=True, port=5555)
    scheduler.stop()
    _LISTEN.stop_stream()
    _LISTEN.shutdown()
