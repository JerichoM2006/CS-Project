import DesktopRecording
import Threadpool
import PrimitiveTranscription
from deep_translator import GoogleTranslator

def main():
    pool = Threadpool.Threadpool(10)
    recording = DesktopRecording.desktopRecording(pool)
    transcriptionAI = PrimitiveTranscription.Transcription("ja-JP")
    translator = GoogleTranslator()

    recording.startRecording()

    while True:
        if recording.buffer.qsize() > 0:
            transcript = transcriptionAI.createTranscript(recording.channels, 
                                                    recording.p.get_sample_size(recording.format), 
                                                    recording.rate, 
                                                    recording.getSegment())

            translated = translator.translate(transcript, src="ja", dest="en")
            if translated == None:
                translated = "..."

            print(translated, end=" ")
            

if __name__ == "__main__":
    main()