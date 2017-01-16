from sirbarksalot.lib.scheduler import Scheduler 
from sirbarksalot.listener.listen import Listener 
from sirbarksalot.listener.specgram import create_spectrogram, write_to_png
def main():
    _listen = Listener()
    _listen.start_stream()
    data = _listen.record()
    _listen.stop_stream()
    _listen.shutdown()

    #_listen.write_to_file(data, "./clips/testclip.wav")
    P, freqs, bins = create_spectrogram(data)
    write_to_png(P, "./clips/testclip_image.png")

if __name__ == "__main__":
    main()