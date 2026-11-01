# ===============================================
# Configurando o texto da LLM
# ===============================================
import json
from datetime import date, datetime
from decimal import Decimal
from ecommerce_intelligence.ai.business_context import get_business_context
from ecommerce_intelligence.ai.llm.factory import get_llm_provider
from ecommerce_intelligence.ai.schemas import BUSINESS_BRIEF_SCHEMA


def serialize_context(context: dict) -> str:

    def serializer(value):

        if isinstance(value, Decimal):
            return float(value)

        if isinstance(value, (date, datetime)):
            return value.isoformat()

        raise TypeError(
            f"Tipo não serializável: {type(value)}"
        )

    return json.dumps(
        context,
        default=serializer,
        ensure_ascii=False,
        indent=2,
    )


def build_prompt(context: dict) -> str:

    enriched_context = {
        **context,

        "analysis_metadata": {
            "granularity": "daily",
            "comparison_type": "previous_day",
            "available_dimensions": [
                "product_category",
                "customer_state",
                "payment_method",
                "delivery_status",
            ],
        },
    }

    context_json = serialize_context(enriched_context)

    return f"""
Você é um analista de negócios especializado em e-commerce.

Sua função é interpretar indicadores previamente calculados
pela plataforma de dados.

REGRAS OBRIGATÓRIAS:

- Utilize exclusivamente os indicadores fornecidos.
- Considere todos os indicadores fornecidos como previamente
  calculados e validados pela plataforma.
- Não recalcule nenhum indicador.
- Não questione a validade matemática dos indicadores.
- Não invente informações.
- Não atribua causalidade sem evidência nos dados.
- Diferencie fatos observados de hipóteses.
- Campos terminados em "_pct" representam percentuais.
- Campos terminados em "_pp" representam pontos percentuais.
- Não confunda valores absolutos com percentuais.
- Quando a causa de uma mudança não estiver nos dados,
  diga que ela precisa ser investigada.
- Recomende investigações, mas não invente suas conclusões.
- Seja objetivo e executivo.
- Não sugira causas específicas que não estejam representadas
  nos indicadores fornecidos.
- Ao relacionar indicadores, descreva apenas relações observadas.
  Não interprete correlação como causa.

RECOMENDAÇÕES DE INVESTIGAÇÃO:
- Recomende apenas análises que possam ser realizadas a partir
  das dimensões disponíveis nos dados.
- Não apresente possíveis explicações para a variação.
- Formule recomendações no formato:
  "Analisar [métrica] por [dimensão disponível] para identificar
  onde a variação está concentrada."
- Não presuma campanhas, promoções, alterações de preço,
  mudanças operacionais ou mudanças de sistema sem evidência
  explícita nos dados.

Para cada sinal:

- "direction" deve ser "up", "down" ou "stable".
- "severity" deve ser "low", "medium" ou "high".
- A severidade representa relevância analítica do sinal,
  não certeza causal.
  
INDICADORES:

{context_json}
"""


def generate_business_brief(context: dict) -> dict:

    llm = get_llm_provider()

    prompt = build_prompt(context)

    response = llm.generate(
        prompt,
        response_format=BUSINESS_BRIEF_SCHEMA,
    )

    return json.loads(response)


def main():

    context = get_business_context()

    brief = generate_business_brief(context)

    print(brief)


if __name__ == "__main__":
    main()