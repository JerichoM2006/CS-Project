import DesktopRecording
import Threadpool
import PrimitiveTranscription
import TranslationAI

def main():
    origLanguage = "ja-JP"
    finalLanguage = "en-US"

    pool = Threadpool.Threadpool(10)
    recording = DesktopRecording.desktopRecording(pool)
    transcriptionAI = PrimitiveTranscription.Transcription(pool, recording, origLanguage)
    translator = TranslationAI.TranslationAI(pool, transcriptionAI, origLanguage, finalLanguage)

    recording.startRecording()
    transcriptionAI.startGeneration()
    translator.startTranslation()

    while True:
        if translator.translationBuffer.qsize() > 0:
            translated = translator.getTranslation()
            print(translated, end=" ")
            

if __name__ == "__main__":
    main()