import speech_recognition as sr
import pyttsx3

class VoiceUtils:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.speaker = pyttsx3.init()

    def listen(self):
        with sr.Microphone() as mic:
            print("Listening...")
            audio = self.recognizer.listen(mic)
            try:
                speech = self.recognizer.recognize_google(audio)
                return speech
            except sr.UnknownValueError:
                print("Could not understand audio.")
                return None
            except sr.RequestError:
                print("Could not request results.")
                return None

    def speak(self, text):
        self.speaker.say(text)
        self.speaker.runAndWait()

def text_to_speech(text):
    try:
        speaker = pyttsx3.init()
        speaker.say(text)
        speaker.runAndWait()
    except Exception as e:
        print(f"Error during text-to-speech: {e}")