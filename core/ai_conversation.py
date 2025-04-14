import openai

class AIConversation:
    def __init__(self):
        openai.api_key = "lm-studio"
        openai.api_base = "http://172.20.128.1:3000/v1"
        self.messages = []

    def chat_with_ai(self, user_message):
        try:
            self.messages.append({"role": "user", "content": user_message})

            response = openai.ChatCompletion.create(
                model="meta-llama-3.1-8b-instruct",
                messages=self.messages,
                stream=True  # Cho phép stream phản hồi
            )

            full_reply = ""
            for chunk in response:
                if "choices" in chunk:
                    delta = chunk["choices"][0]["delta"]
                    if "content" in delta:
                        content_piece = delta["content"]
                        full_reply += content_piece
                        yield content_piece  # Trả từng phần nhỏ ra ngoài

            self.messages.append({"role": "assistant", "content": full_reply})

        except Exception as e:
            yield f"[Error]: {str(e)}"
