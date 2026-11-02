# ===============================================
# Configurando o provedor Ollama
# ===============================================
from ollama import Client

from ecommerce_intelligence.ai.llm.base import LLMProvider


class OllamaProvider(LLMProvider):

    provider_name = "ollama"

    def __init__(
        self,
        model: str,
        base_url: str,
    ):
        self.model = model
        self.base_url = base_url.rstrip("/")

        self.client = Client(
            host=self.base_url
        )

    def generate(
        self,
        prompt: str,
        response_format: dict | None = None,
    ) -> str:

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            format=response_format,
        )

        return response["message"]["content"]