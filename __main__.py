import DesktopRecording
import Threadpool
import PrimitiveTranscription
from deep_translator import GoogleTranslator

def main():
    origLanguage = "ja-JP"
    finalLanguage = "en-US"

    pool = Threadpool.Threadpool(10)
    recording = DesktopRecording.desktopRecording(pool)
    transcriptionAI = PrimitiveTranscription.Transcription(pool, recording, origLanguage)
    translator = GoogleTranslator()

    recording.startRecording()
    transcriptionAI.startGeneration()

    while True:
        if transcriptionAI.transcriptBuffer.qsize() > 0:
            transcript = transcriptionAI.getTranscript()

            translated = translator.translate(transcript, src=origLanguage, dest=finalLanguage)
            if translated == None:
                translated = "..."

            print(translated, end=" ")
            

if __name__ == "__main__":
    main()