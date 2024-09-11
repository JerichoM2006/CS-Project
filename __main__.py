import DesktopRecording
import Threadpool

def main():
    pool = Threadpool.Threadpool(10)
    recording = DesktopRecording.desktopRecording(pool)
    recording.startRecording()

    while True:
        inp = input("1. Get from buffer\n2. Get buffer length\n3. Stop recording\n")

        if inp == "1":
            print(recording.getSegment())
        elif inp == "2":
            print(recording.buffer.qsize())
        elif inp == "3":
            recording.stopRecording()
            break

if __name__ == "__main__":
    main()