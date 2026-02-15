import requests


class PerplexityClient:
    def __init__(self):

        self.api_key = "pplx-****"

        if not self.api_key or self.api_key.strip() == "":
            raise ValueError(
                "Perplexity API key is empty. Insert your key into perplexity_api.py"
            )

        self.url = "https://api.perplexity.ai/chat/completions"
        self.model = "sonar-pro"

    def ask(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "max_tokens": 800,
        }

        response = requests.post(self.url, json=payload, headers=headers)
        response.raise_for_status()

        data = response.json()
        return data["choices"][0]["message"]["content"]
