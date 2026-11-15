# =====================================================
# Gerador de datas = Processamento incremental
# =====================================================
# Bibliotecas
from datetime import date, timedelta
import pandas as pd


def get_reference_date() -> date:
    """Retorna o dia anterior à execução como data de referência.

    Returns
    -------
    date
        Última data considerada para a geração incremental.
    """
    return date.today() - timedelta(days=1)


def get_missing_dates(
    last_generated_date: date | None,
    reference_date: date,
    start_date: date = date(2024, 1, 1),
) -> list[date]:
    """Identifica as datas ainda não processadas até a referência.

    Parameters
    ----------
    last_generated_date:
        Última data já existente no histórico; None para carga inicial.

    reference_date:
        Data limite, incluída no processamento.

    start_date:
        Data inicial utilizada quando não existe histórico.

    Returns
    -------
    list[date]
        Datas faltantes em ordem cronológica.
    """

    # Inicia na data padrão ou no dia seguinte ao último registro.
    if last_generated_date is None:
        next_date = start_date
    else:
        next_date = last_generated_date + timedelta(days=1)

    if next_date > reference_date:
        return []

    # Retorna somente os dias ainda não contemplados no histórico.
    return [
        timestamp.date()
        for timestamp in pd.date_range(
            start=next_date,
            end=reference_date,
            freq="D",
        )
    ]
