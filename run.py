from sirbarksalot.lib.scheduler import Scheduler
from sirbarksalot.listener.listen import Listener
from sirbarksalot.listener.specgram import create_spectrogram, write_to_png
from sirbarksalot.detector.match import MatchTemplate
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

_LISTEN = Listener()
_LISTEN.start_stream()
def send_message(corr):
    payload = {
        'recipient': {'phone_number': PHONE_NUMBER},
        'message': {'text': 'woof woof: {:.4f}'.format(corr)}
    }

    headers = {'Content-Type': 'application/json'}
    print payload
    r = requests.post(URL, json=payload, headers=headers)
    print r

def listen():

    # get some data
    data = _LISTEN.record()

    # make a spectrogram
    _specgram = create_spectrogram(data)
    score = _MT.calculate_score(_specgram)

    # write it out
    if score > 0.75:
        logger.info("Bark Found! Correlation: {}".format(score))
        _ms = "{0}".format(time.time()).split(".")[0]
        _LISTEN.write_to_file(data, make_filename("wav", _ms))
        # write_to_png(_specgram, make_filename("png", _ms))
        send_message(score)
        return 1
    return 0


app = create_app()

if __name__ == "__main__":
    scheduler = Scheduler(6, listen)
    scheduler.start()
    app.run(debug=True, port=5555)
    scheduler.stop()
    _LISTEN.stop_stream()
    _LISTEN.shutdown()
