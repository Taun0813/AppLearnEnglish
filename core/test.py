import os

audio_path = "data/tts/Conversation-1-Challenge-12.mp3"
absolute_audio_path = os.path.abspath(audio_path)

# Kiểm tra xem tệp có tồn tại không
if os.path.exists(absolute_audio_path):
    print(f"Tệp âm thanh tồn tại: {absolute_audio_path}")
else:
    print(f"Không tìm thấy tệp âm thanh: {absolute_audio_path}")
