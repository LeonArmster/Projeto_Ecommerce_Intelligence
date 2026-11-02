# ===============================================
# Configurando o texto da LLM
# ===============================================
import json
from datetime import date, datetime
from decimal import Decimal
import logging
import time
from ecommerce_intelligence.config.logger import configure_logger
from ecommerce_intelligence.ai.business_context import get_business_context
from ecommerce_intelligence.ai.llm.factory import get_llm_provider
from ecommerce_intelligence.ai.brief_repository import save_business_brief
from ecommerce_intelligence.ai.schemas import BUSINESS_BRIEF_SCHEMA



# Configurando o logger
logger = logging.getLogger(__name__)

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

  SINAIS ANALÍTICOS:

- O campo "metric_signals" contém classificações calculadas
  deterministicamente pela plataforma.
- "direction" e "severity" já foram definidos pela plataforma.
- Não altere essas classificações.
- Utilize essas informações para priorizar a interpretação.
  
INDICADORES:

{context_json}
"""


def generate_business_brief(
    context: dict,
    llm,
) -> dict:

    prompt = build_prompt(context)

    response = llm.generate(
        prompt,
        response_format=BUSINESS_BRIEF_SCHEMA,
    )

    return json.loads(response)


def main():

    configure_logger()

    start_time = time.perf_counter()

    logger.info("Iniciando geração do Business Brief")

    try:

        # -----------------------------
        # Business Context
        # -----------------------------

        logger.info("Carregando Business Context")

        context = get_business_context()

        reference_date = context["order_date"]

        logger.info(
            "Business Context carregado | reference_date=%s",
            reference_date,
        )

        # -----------------------------
        # LLM
        # -----------------------------

        llm = get_llm_provider()

        logger.info(
            "LLM configurado | provider=%s | model=%s",
            llm.provider_name,
            llm.model,
        )

        logger.info("Gerando Business Brief")

        llm_start = time.perf_counter()

        brief = generate_business_brief(
            context=context,
            llm=llm,
        )

        llm_duration = time.perf_counter() - llm_start

        logger.info(
            "Business Brief gerado | "
            "llm_duration_seconds=%.2f",
            llm_duration,
        )

        # -----------------------------
        # Persistence
        # -----------------------------

        logger.info(
            "Persistindo Business Brief"
        )

        save_business_brief(
            reference_date=reference_date,
            provider=llm.provider_name,
            model_name=llm.model,
            context=context,
            brief=brief,
            generation_duration_seconds=llm_duration,
        )

        duration = time.perf_counter() - start_time

        logger.info(
            "Business Brief persistido | "
            "reference_date=%s | "
            "provider=%s | "
            "model=%s | "
            "duration_seconds=%.2f",
            reference_date,
            llm.provider_name,
            llm.model,
            duration,
        )

    except Exception:

        duration = time.perf_counter() - start_time

        logger.exception(
            "Falha na geração do Business Brief | "
            "duration_seconds=%.2f",
            duration,
        )

        raise


if __name__ == "__main__":
    main()