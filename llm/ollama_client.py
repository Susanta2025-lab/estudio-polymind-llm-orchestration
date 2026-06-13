import requests


class OllamaClient:

    def __init__(
        self,
        model="mistral"
    ):

        self.model = model
        self.url = (
            "http://localhost:11434/api/chat"
        )

    def generate(
        self,
        prompt: str
    ) -> str:

        payload = {

            "model": self.model,

            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            "stream": False
        }

        response = requests.post(
            self.url,
            json=payload
        )

        if response.status_code != 200:
            raise Exception(
                response.text
            )

        return response.json()[
            "message"
        ]["content"]

    def generate_stream(
        self,
        prompt: str
    ):

        payload = {

            "model": self.model,

            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            "stream": True
        }

        response = requests.post(
            self.url,
            json=payload,
            stream=True
        )

        if response.status_code != 200:
            raise Exception(
                response.text
            )

        for line in response.iter_lines():

            if not line:
                continue

            data = (
                line.decode("utf-8")
            )

            try:

                import json

                chunk = json.loads(
                    data
                )

                if (
                    "message"
                    in chunk
                ):

                    yield chunk[
                        "message"
                    ][
                        "content"
                    ]

            except Exception:
                continue
