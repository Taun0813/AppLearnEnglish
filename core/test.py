# import os
# import pygame
#
# audio_path = "../data/tts/Conversation-1-Challenge-1.wav"
# absolute_audio_path = os.path.abspath(audio_path)
#
# # Initialize pygame mixer
# pygame.mixer.init()
#
# # Load the mp3 file
# def play_audio(file_path):
#     try:
#         pygame.mixer.music.load(file_path)
#         pygame.mixer.music.play()
#         while pygame.mixer.music.get_busy():
#             pygame.time.Clock().tick(10)  # Check every 10 ms if music is playing
#     except pygame.error as e:
#         print(f"Error playing audio: {e}")
#
# # Kiểm tra xem tệp có tồn tại không
# if os.path.exists(absolute_audio_path):
#     print(f"Tệp âm thanh tồn tại: {absolute_audio_path}")
#     # Phát âm thanh
#     play_audio(absolute_audio_path)
#
# else:
#     print(f"Không tìm thấy tệp âm thanh: {absolute_audio_path}")

import os
import glob

folder_path = "F:/DoAnChuyenNganh/AI/data/tts"

mp3_files = glob.glob(os.path.join(folder_path, "*.mp3"))

for file in mp3_files:
    try:
        os.remove(file)
        print(f"🗑️ Deleted: {file}")
    except Exception as e:
        print(f"❌ Error deleting {file}: {e}")

