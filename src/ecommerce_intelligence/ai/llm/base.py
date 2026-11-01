# ===============================================
# Configurando a base de trabalho do LLM
# ===============================================
from abc import ABC, abstractmethod


class LLMProvider(ABC):

    @abstractmethod
    def generate(
        self,
        prompt: str,
        response_format: dict | None = None,
    ) -> str:
        pass