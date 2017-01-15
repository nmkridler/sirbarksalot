import pyaudio
import wave 

def main():
    params = {
        "frames_per_buffer": 1024,
        "format": pyaudio.paInt16,
        "rate": 44100,
        "channels": 2,
        "input": True
    }

    p = pyaudio.PyAudio()

    stream = p.open(**params)
    print "recording..."

    frames = []
    for i in range(0, int(params["rate"] / params["frames_per_buffer"] * 5)):
        data = stream.read(params["frames_per_buffer"])
        frames.append(data)
    
    print "done recording."

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open("test.wave", 'wb')
    wf.setnchannels(params["channels"])
    wf.setsampwidth(p.get_sample_size(params["format"]))
    wf.setframerate(params["rate"])
    wf.writeframes(b''.join(frames))
    wf.close()

if __name__ == "__main__":
    main()