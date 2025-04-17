from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import os
import json
import pyttsx3
import subprocess



# Hàm lưu dữ liệu theo định dạng JSON
def save_to_json(data, file_name):
    os.makedirs('data', exist_ok=True)
    with open(file_name, 'w') as json_file:
        json.dump(data, json_file, indent=4)


# Hàm crawl DailyDictation và lấy dữ liệu
def crawl_dailydictation(url):
    """
    Crawls the specified DailyDictation URL to extract audio URLs, spoken texts, and answers.

    Args:
        url: The URL of the DailyDictation exercise page.

    Returns:
        A dictionary where keys are challenge IDs (e.g., "Challenge #1") and values
        are dictionaries containing:
            - audio_url: The URL of the audio file.
            - spoken_text: The transcribed spoken text.
            - answer: The correct answer text.
    """
    data = {}
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        audio_element = soup.find('audio', class_='my-3')
        audio_url = audio_element.find('source')['src'] if audio_element and audio_element.find('source') else None
        audio_url = audio_url if audio_url and audio_url.startswith('http') else urljoin(url, audio_url) if audio_url else None

        transcript_div = soup.find('div', id='transcriptAccordionItem')
        challenges = {}

        if transcript_div:
            text_divs = transcript_div.find_all('div', title=True)

            for text_div in text_divs:
                challenge_id = text_div['title']
                spoken_text = text_div.get_text(strip=True)

                challenges[challenge_id] = {
                    "spoken_text": spoken_text,
                    "audio_path": ""  # Path will be added later when generating audio.
                }

        data["audio_url"] = audio_url
        data["Challenges"] = challenges

        return data
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {}



# Hàm crawl các link bài tập từ DailyDictation
def get_all_conversation_links(base_url):
    """
    Crawls the base URL to get all conversation links.
    """
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        links = []
        for link in soup.find_all('a', href=True):
            if '/exercises/toeic/conversation-' in link['href']:
                full_url = urljoin(base_url, link['href'])
                if full_url not in links:
                    links.append(full_url)
        return links
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []


def generate_audio_from_text(data_file, output_dir):
    """
    Generates .wav audio files from text using pyttsx3 and ffmpeg.
    Also updates JSON with the relative path of generated audio files.

    Args:
        data_file: Path to the JSON file containing the text data.
        output_dir: Directory to save the generated audio files.
    """
    os.makedirs(output_dir, exist_ok=True)

    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: Data file not found at {data_file}")
        return
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON format in {data_file}")
        return

    engine = pyttsx3.init()
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    for conversation_url, conversation_data in data.items():
        challenges = conversation_data.get("Challenges", {})
        conversation_name = conversation_url.replace('/', '').replace(':', '')

        for challenge_id, challenge_data in challenges.items():
            spoken_text = challenge_data.get('spoken_text', '').strip()
            if not spoken_text:
                continue

            clean_challenge = challenge_id.replace('#', '').replace(' ', '-')
            output_filename_mp3 = f"{conversation_name}-{clean_challenge}.mp3"
            output_path_mp3 = os.path.join(output_dir, output_filename_mp3)

            output_filename_wav = output_filename_mp3.replace(".mp3", ".wav")
            output_path_wav = os.path.join(output_dir, output_filename_wav)

            if not os.path.exists(output_path_wav):
                try:
                    # Step 1: Generate MP3
                    engine.save_to_file(spoken_text, output_path_mp3)
                    engine.runAndWait()

                    # Step 2: Convert MP3 to WAV
                    subprocess.run([
                        "ffmpeg", "-y", "-i", output_path_mp3, output_path_wav
                    ], check=True)
                    print(f"🎧 Converted to WAV: {output_path_wav}")

                    # Step 3: Delete MP3
                    os.remove(output_path_mp3)
                    print(f"🗑️ Deleted MP3: {output_path_mp3}")

                except Exception as e:
                    print(f"❌ Error processing {challenge_id}: {e}")
                    continue
            else:
                print(f"✅ WAV already exists: {output_path_wav}")

            # Step 4: Update JSON with relative WAV path
            relative_path = os.path.relpath(output_path_wav, start=base_dir).replace("\\", "/")
            challenge_data["audio_path"] = relative_path

    # Step 5: Save updated JSON
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"💾 Updated JSON saved to {data_file}")

# def generate_audio_from_text(data_file, output_dir):
#     """
#     Generates audio files from text using pyttsx3, converts to .wav using pydub, and deletes original .mp3.
#     """
#     os.makedirs(output_dir, exist_ok=True)
#
#     try:
#         with open(data_file, 'r', encoding='utf-8') as f:
#             data = json.load(f)
#     except FileNotFoundError:
#         print(f"Error: Data file not found at {data_file}")
#         return
#     except json.JSONDecodeError:
#         print(f"Error: Invalid JSON format in {data_file}")
#         return
#
#     engine = pyttsx3.init()
#
#     base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
#
#     for conversation_url, conversation_data in data.items():
#         challenges = conversation_data.get("Challenges", {})
#         conversation_name = conversation_url
#
#         for challenge_id, challenge_data in challenges.items():
#             spoken_text = challenge_data.get('spoken_text', '').strip()
#             if not spoken_text:
#                 continue
#
#             clean_challenge = challenge_id.replace('#', '').replace(' ', '-')
#
#             mp3_filename = f"{conversation_name}-{clean_challenge}.mp3"
#             wav_filename = f"{conversation_name}-{clean_challenge}.wav"
#
#             mp3_path = os.path.join(output_dir, mp3_filename)
#             wav_path = os.path.join(output_dir, wav_filename)
#
#             if not os.path.exists(wav_path):
#                 try:
#                     engine.save_to_file(spoken_text, mp3_path)
#                     engine.runAndWait()
#                     print(f"[TTS] Audio saved: {mp3_path}")
#
#                     # Convert mp3 to wav
#                     audio = AudioSegment.from_file(mp3_path, format="mp3")
#                     audio.export(wav_path, format="wav")
#                     print(f"[Convert] Converted to WAV: {wav_path}")
#
#                     # Remove mp3 file
#                     os.remove(mp3_path)
#                     print(f"[Clean] Removed MP3: {mp3_path}")
#                 except Exception as e:
#                     print(f"Error generating audio for {challenge_id}: {e}")
#                     continue
#             else:
#                 print(f"[Skip] WAV already exists: {wav_path}")
#
#             # Cập nhật đường dẫn tương đối
#             relative_path = os.path.relpath(wav_path, start=base_dir).replace("\\", "/")
#             challenge_data["audio_path"] = relative_path
#
#     with open(data_file, 'w', encoding='utf-8') as f:
#         json.dump(data, f, indent=4, ensure_ascii=False)


def main():
    base_url = "https://dailydictation.com/exercises/toeic"
    conversation_links = get_all_conversation_links(base_url)

    # Chỉ lấy 50 topic đầu tiên
    conversation_links = conversation_links[:50]

    all_data = {}
    for link in conversation_links:
        print(f"Crawling: {link}")
        data = crawl_dailydictation(link)

        from urllib.parse import urlparse
        path = urlparse(link).path.lstrip('/')
        # Lấy conversation số
        import re
        match = re.search(r'conversation-(\d+)', path)
        if match:
            conv_number = match.group(1)
            short_key = f"Conversation-{conv_number}"
            all_data[short_key] = data

    # Lưu dữ liệu vào listen.json
    with open('../data/listen.json', 'w') as f:
        json.dump(all_data, f, indent=4)

    # Tạo âm thanh từ văn bản và cập nhật đường dẫn vào listen.json
    generate_audio_from_text('../data/listen.json', '../data/tts')



if __name__ == "__main__":
    main()
