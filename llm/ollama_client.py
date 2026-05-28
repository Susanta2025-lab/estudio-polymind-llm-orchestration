import requests

class OllamaClient:
    def __init__(self, model="mistral"):
        self.model = model
        self.url = "http://localhost:11434/api/chat"

    def generate(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }

        response = requests.post(self.url, json=payload)

        if response.status_code != 200:
            raise Exception(response.text)

        return response.json()["message"]["content"]
