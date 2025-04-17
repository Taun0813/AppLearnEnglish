from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import json
import os
import pyttsx3


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
    Generates audio files from text using pyttsx3.

    Args:
        data_file: Path to the JSON file containing the text data.
        output_dir: Directory to save the generated audio files.
    """
    os.makedirs(output_dir, exist_ok=True)

    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Data file not found at {data_file}")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {data_file}")
        return

    engine = pyttsx3.init()

    # Gốc thư mục cha để chuẩn hóa relative path
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    for conversation_url, conversation_data in data.items():
        challenges = conversation_data.get("Challenges", {})

        # Lấy tên Conversation (VD: Conversation1 từ https://.../Conversation1.1481/listen-and-type)
        conversation_name = conversation_url

        for challenge_id, challenge_data in challenges.items():
            spoken_text = challenge_data.get('spoken_text', '').strip()
            if not spoken_text:
                continue  # Bỏ qua nếu không có text

            # Đổi "Challenge #1" → "Challenge-1"
            clean_challenge = challenge_id.replace('#', '').replace(' ', '-')

            # Tạo tên file: Conversation1-Challenge-1.mp3
            output_filename = f"{conversation_name}-{clean_challenge}.mp3"
            output_path = os.path.join(output_dir, output_filename)

            if not os.path.exists(output_path):
                try:
                    engine.save_to_file(spoken_text, output_path)
                    engine.runAndWait()
                    print(f"Audio saved to: {output_path}")
                except Exception as e:
                    print(f"Error generating audio for {challenge_id}: {e}")
                    continue
            else:
                print(f"Audio file already exists: {output_path}")

            # Cập nhật lại đường dẫn tương đối cho JSON
            relative_path = os.path.relpath(output_path, start=base_dir).replace("\\", "/")
            challenge_data["audio_path"] = relative_path

    # Lưu lại file JSON với các audio_path đã cập nhật
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


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
