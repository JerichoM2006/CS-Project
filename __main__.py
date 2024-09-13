import DesktopRecording
import Threadpool
import PrimitiveTranscription

def main():
    pool = Threadpool.Threadpool(10)
    recording = DesktopRecording.desktopRecording(pool)
    transcriptionAI = PrimitiveTranscription.Transcription()
    recording.startRecording()

    while True:
        if recording.buffer.qsize() > 0:
            transcript = transcriptionAI.createTranscript(recording.channels, 
                                                    recording.p.get_sample_size(recording.format), 
                                                    recording.rate, 
                                                    recording.getSegment())
            
            print(transcript, end=" ")
            

if __name__ == "__main__":
    main()