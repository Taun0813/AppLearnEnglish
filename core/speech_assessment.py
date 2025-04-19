import speech_recognition as sr

class SpeechAssessment:
    def assess_pronunciation(self, audio_data, text_reference):
        recognizer = sr.Recognizer()
        try:
            audio = sr.AudioData(audio_data, sample_rate=44100, sample_width=2)
            text = recognizer.recognize_google(audio, language="en-US")
            feedback = f"You said: {text}"
            return {'score': 0.0, 'feedback': feedback}
        except sr.UnknownValueError:
            return {'score': 0.0, 'feedback': "Could not understand audio."}
        except sr.RequestError as e:
            return {'score': 0.0, 'feedback': f"Speech recognition service error: {e}"}

def evaluate(audio_path, reference_text):
    import whisper
    import difflib

    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    user_text = result["text"].strip()

    # Đơn giản: tính độ giống nhau
    ratio = difflib.SequenceMatcher(None, reference_text.lower(), user_text.lower()).ratio()
    score = round(ratio * 100, 2)

    feedback = "Tốt!" if score >= 80 else "Cần luyện thêm!"

    return {
        "score": score,
        "feedback": feedback,
        "user_text": user_text
    }







