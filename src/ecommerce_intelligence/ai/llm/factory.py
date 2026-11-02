# ===============================================
# Configurando o modelo de LLM que será usado
# ===============================================
import os
from ecommerce_intelligence.ai.llm.base import LLMProvider
from ecommerce_intelligence.ai.llm.ollama import OllamaProvider


def get_llm_provider() -> LLMProvider:

    provider = os.getenv(
        "LLM_PROVIDER",
        "ollama",
    ).lower()

    if provider == "ollama":

        return OllamaProvider(
            model=os.getenv(
                "OLLAMA_MODEL",
                "qwen3:8b",
            ),
            base_url=os.getenv(
                "OLLAMA_BASE_URL",
                "http://localhost:11434",
            ),
        )

    raise ValueError(
        f"LLM provider não suportado: {provider}"
    )



# llm = get_llm_provider()

# response = llm.generate(
#     "Explique em uma frase o que é ticket médio em e-commerce."
# )

# print(response)