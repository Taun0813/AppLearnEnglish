import speech_recognition as sr
import whisper
import numpy as np

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

# Load the model
model = whisper.load_model("base")

def evaluate(audio_path, reference_text):
    """
    Evaluate the speech of a user in an audio file.

    Args:
      audio_path: The path of the user audio
      reference_text: the reference text

    Returns:
      result: The score and feedback of the user
    """

    print(f'evaluate - start')

    result = model.transcribe(audio_path)

    # get the text
    user_text = result["text"]

    # score calculation (this is an example, you can improve this part)
    score = len(user_text.split()) / len(reference_text.split())

    if score > 1:
      score = 1
    if score < 0:
      score = 0

    print(f'evaluate - end')
    # feedback generation
    feedback = 'Your score is : ' + str(score) + ' user text is : '+ user_text

    return {
        "score": score,
        "feedback": feedback,
        "user_text": user_text,
    }






