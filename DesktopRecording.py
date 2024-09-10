import pyaudio
import wave
import numpy as np

sound  = True
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "output.wav"

volume = 35

p = pyaudio.PyAudio()


stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index = 2,
                frames_per_buffer=CHUNK)
print("recording...")


frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    audio_data = np.frombuffer(data, dtype=np.int16)
    
    audio_data = (audio_data * volume).astype(np.int16)
    
    frames.append(audio_data.tobytes())


print("finished recording")
stream.stop_stream()
stream.close()
p.terminate()
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()