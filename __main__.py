import DesktopRecording
import Threadpool
import wave
import os

def main():
    pool = Threadpool.Threadpool(10)
    recording = DesktopRecording.desktopRecording(pool)
    recording.startRecording()

    while True:
        inp = input("1. Get from buffer\n2. Get buffer length\n3. Stop recording\n")

        if inp == "1":
            print("Segment fetched")

            name = "segment"
            index = 1
            while os.path.exists(name + str(index) + ".wav"):
                index += 1
            name =name + str(index) + ".wav"

            waveFile = wave.open(name, 'wb')
            waveFile.setnchannels(recording.channels)
            waveFile.setsampwidth(recording.p.get_sample_size(recording.format))
            waveFile.setframerate(recording.rate)
            waveFile.writeframes(recording.getSegment())
            waveFile.close()
        elif inp == "2":
            print("Buffer length: ", recording.buffer.qsize())
        elif inp == "3":
            recording.stopRecording()
            break

if __name__ == "__main__":
    main()