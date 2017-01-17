"""
"""
import wave
import pyaudio
from scipy.io import wavfile
import numpy as np

def calculate_buffer_size(rate, frames_per_buffer, sample_length):
    """ calculate the buffer size

        Args:
            rate (int): sampling rate
            frames_per_buffer (int): number of frames per buffer
            sample_length (int): number of samples to collect
    """
    return (rate / frames_per_buffer) * sample_length

class Listener(object):
    _config = {
        "frames_per_buffer": 1024,
        "format": pyaudio.paInt16,
        "rate": 44100,
        "channels": 1,
        "input": True
    }
    def __init__(self, sample_length=5):
        self.input = pyaudio.PyAudio()
        self.stream = None
        self.n_frames = calculate_buffer_size(
            self._config["rate"],
            self._config["frames_per_buffer"],
            sample_length
        )

    def start_stream(self):
        self.stream = self.input.open(**self._config)

    def stop_stream(self):
        self.stream.close()

    def shutdown(self):
        self.input.terminate()

    def record(self):
        """"""
        i, frames = 0, []
        while i < self.n_frames:
            data = self.stream.read(self._config["frames_per_buffer"])
            frames.append(data)
            i += 1
        return np.fromstring(b''.join(frames), dtype=np.int16)

    def write_to_file(self, data, filename):
        """"""
        wavfile.write(filename, self._config["rate"], data)
