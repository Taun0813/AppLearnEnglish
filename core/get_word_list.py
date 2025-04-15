from selenium import webdriver
from selenium.webdriver.common.by import By
import json

driver = webdriver.Chrome()
url = "https://vn.elsaspeak.com/tu-vung-tieng-anh-giao-tiep-co-ban-theo-chu-de/"
driver.get(url)
driver.implicitly_wait(5)

# Lấy danh sách chủ đề (topic)
topics = []
titles = driver.find_elements(By.CLASS_NAME, "wp-block-heading")
for title in titles:
    if title.text.strip():
        topics.append(title.text.strip())

# Loại bỏ các topic không cần
indexes_to_remove = [0, 1, 22, 23, 24, 25]
filtered_topics = [t for i, t in enumerate(topics) if i not in indexes_to_remove]

# Lấy tất cả các bảng từ vựng
tables = driver.find_elements(By.TAG_NAME, "table")

# Tạo danh sách dữ liệu theo topic
all_topics_data = []

for i, table in enumerate(tables):
    topic = filtered_topics[i] if i < len(filtered_topics) else f"Topic {i + 1}"
    words = []

    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows[1:]:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) >= 4:
            word = cols[0].text.strip()
            pronunciation = cols[1].text.strip()
            word_type = cols[2].text.strip()
            meaning = cols[3].text.strip()
            words.append({
                "word": word,
                "pronunciation": pronunciation,
                "word_type": word_type,
                "meaning": meaning
            })

    topic_data = {
        "topic": topic,
        "words": words
    }
    all_topics_data.append(topic_data)

# # Đảm bảo thư mục tồn tại
# os.makedirs("data", exist_ok=True)

# Lưu ra file vocab.json
with open("../data/vocab.json", "w", encoding="utf-8") as f:
    json.dump(all_topics_data, f, ensure_ascii=False, indent=2)

driver.quit()
print("Đã lưu", len(all_topics_data), "chủ đề từ vựng.")
