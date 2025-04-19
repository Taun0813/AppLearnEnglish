import speech_recognition as sr
from core.speech_assessment import SpeechAssessment

def test_speech_to_text():
    recognizer = sr.Recognizer()
    assessment = SpeechAssessment()

    with sr.Microphone() as source:
        print("Please speak for 5 seconds...")
        audio = recognizer.listen(source, timeout=5)

    print("Transcribing...")
    result = assessment.assess_pronunciation(audio.get_wav_data(), "")  # Corrected line
    print("Transcription:", result["feedback"])

if __name__ == "__main__":
    test_speech_to_text()