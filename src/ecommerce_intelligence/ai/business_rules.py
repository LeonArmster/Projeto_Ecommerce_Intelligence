# ============================================================
# Regras de negócio para classificação dos indicadores
# ============================================================

# ------------------------------------------------------------
# Thresholds de severidade por indicador
# ------------------------------------------------------------
# IMPORTANTE:
# Estes valores são regras de demonstração do projeto.
# Não representam benchmarks universais de e-commerce.
SEVERITY_RULES = {
    "net_sales_change_pct": {
        "medium": 0.05,
        "high": 0.10,
    },
    "orders_change_pct": {
        "medium": 0.05,
        "high": 0.10,
    },
    "avg_order_value_change_pct": {
        "medium": 0.03,
        "high": 0.07,
    },
    "cancellation_rate_change_pp": {
        "medium": 1.0,
        "high": 3.0,
    },
    "delay_rate_change_pp": {
        "medium": 2.0,
        "high": 5.0,
    },
    "avg_rating_change": {
        "medium": 0.10,
        "high": 0.30,
    },
}


# ------------------------------------------------------------
# Classificação da severidade
# ------------------------------------------------------------
def classify_severity(
    value: float,
    medium_threshold: float,
    high_threshold: float,
) -> str:
    """
    Classifica a relevância da variação de um indicador.

    A classificação utiliza o valor absoluto porque tanto
    variações positivas quanto negativas podem ser relevantes.
    """

    absolute_value = abs(value)

    if absolute_value >= high_threshold:
        return "high"

    if absolute_value >= medium_threshold:
        return "medium"

    return "low"


# ------------------------------------------------------------
# Classificação da direção
# ------------------------------------------------------------
def classify_direction(value: float) -> str:
    """
    Classifica a direção da variação do indicador.
    """

    if value > 0:
        return "up"

    if value < 0:
        return "down"

    return "stable"


# ------------------------------------------------------------
# Construção dos sinais dos indicadores
# ------------------------------------------------------------
def build_metric_signals(
    context: dict,
) -> list[dict]:
    """
    Gera os sinais estruturados dos indicadores disponíveis
    no contexto de negócio.

    Retorna:
        metric
        value
        direction
        severity
    """

    signals = []

    for metric, thresholds in SEVERITY_RULES.items():

        value = context.get(metric)

        # Caso a métrica não exista no contexto,
        # simplesmente ignoramos.
        if value is None:
            continue

        value = float(value)

        direction = classify_direction(value)

        severity = classify_severity(
            value=value,
            medium_threshold=thresholds["medium"],
            high_threshold=thresholds["high"],
        )

        signals.append(
            {
                "metric": metric,
                "value": value,
                "direction": direction,
                "severity": severity,
            }
        )

    return signals