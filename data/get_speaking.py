import requests
from bs4 import BeautifulSoup
import json

BASE_URL = 'https://www.eslfast.com'


def get_topic_links():
    url = 'https://www.eslfast.com/robot/smalltalk.htm'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    # Lấy tất cả các topic từ trang danh sách
    topic_links = []
    for li in soup.find_all('li'):
        a_tag = li.find('a')
        if a_tag:
            p_tag = a_tag.find('p')
            if p_tag:
                # Lấy phần tên topic từ thẻ span với class "contan"
                topic_name = p_tag.find('span', class_='contan').text.strip()
                topic_url = BASE_URL + a_tag['href']
                topic_links.append({'name': topic_name, 'url': topic_url})

    return topic_links


def get_conversation_from_topic(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    # Lấy audio URL
    audio_tag = soup.find('audio')
    audio_url = BASE_URL + audio_tag['src'] if audio_tag else None

    # Lấy nội dung hội thoại
    dialogue_tag = soup.find('font', {'face': 'arial'})
    dialogue = []
    if dialogue_tag:
        dialogue_text = dialogue_tag.get_text(separator='\n').strip().split('\n')
        speaker = 'A'  # Mặc định người nói đầu tiên là "A"
        for line in dialogue_text:
            if line.strip():
                # Tìm người nói và câu thoại
                if line.startswith('A:'):
                    speaker = 'A'
                    sentence = line[2:].strip()  # Cắt bỏ phần "A:"
                elif line.startswith('B:'):
                    speaker = 'B'
                    sentence = line[2:].strip()  # Cắt bỏ phần "B:"
                else:
                    sentence = line.strip()

                if sentence:
                    dialogue.append({"speaker": speaker, "text": sentence})
                    # Luân phiên giữa A và B
                    speaker = 'B' if speaker == 'A' else 'A'

    return {
        "audio_url": audio_url,
        "dialogue": dialogue
    }


# Lấy tất cả các topic
topics = get_topic_links()
speaking_data = {}

for topic in topics:
    print(f"Processing Topic: {topic['name']}, URL: {topic['url']}")
    conversation_data = get_conversation_from_topic(topic['url'])
    speaking_data[topic['url']] = {
        "topic": topic['name'],
        "audio_url": conversation_data['audio_url'],
        "dialogue": conversation_data['dialogue']
    }

# Lưu dữ liệu vào file speaking.json
with open('speaking.json', 'w', encoding='utf-8') as json_file:
    json.dump(speaking_data, json_file, ensure_ascii=False, indent=4)

print("Data has been saved to speaking.json")
