import pyaudio
import wave
import numpy as np

#Audio open variables
sound  = True
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "output.wav"

#Audio realtime variables
volume = 35
lowerVolumeCutoff = 1.10

p = pyaudio.PyAudio()

deviceIndex = -1
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    if (dev['name'] == 'Stereo Mix (Realtek(R) Audio)' and dev['hostApi'] == 0):
        deviceIndex = dev['index']

if (deviceIndex == -1):
    print("Stereo Mix (Realtek(R) Audio) not found")
    exit(1)
else:
    print("Found Stereo Mix (Realtek(R) Audio) at index " + str(deviceIndex))


stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index = deviceIndex,
                frames_per_buffer=CHUNK)
print("recording...")


frames = []
#for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
while True:
    data = stream.read(CHUNK)
    audio_data = np.frombuffer(data, dtype=np.int16)
    
    rms = np.sqrt(np.mean(np.power(audio_data, 2)))
    print(rms)
    if rms < lowerVolumeCutoff:
        break

    audio_data = (audio_data * volume).astype(np.int16)
    
    frames.append(audio_data.tobytes())

print("finished recording")
stream.stop_stream()
stream.close()
p.terminate()

if len(frames) <= 0:
    print("No sound detected")
    exit(1)

"""
if len(frames) > 0:
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
else:
    print("No sound detected")
"""