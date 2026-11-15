
# ============================================
# Arquivo de conversão de parquet para csv
# ============================================
# Bibliotecas
from pathlib import Path
import pandas as pd


# Colunas auxiliares utilizadas apenas na geração incremental.
EXCLUDED_COLUMNS = {
    "payments": ["scheduled_paid_at"],
    "shipments": [
        "scheduled_shipped_at",
        "scheduled_delivered_at",
    ],
}


def parquet_to_csv(
    source: Path,
    destination: Path,
) -> None:
    """
    Converte um arquivo Parquet para CSV
    utilizado na carga do PostgreSQL.

    Remove as colunas auxiliares utilizadas
    exclusivamente na geração incremental.

    Parameters
    ----------
    source:
        Caminho do arquivo Parquet de origem.

    destination:
        Caminho do arquivo CSV de destino.

    Returns
    -------
    None
    """

    # =================================================
    # 1. Preparar diretório de destino
    # =================================================
    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # =================================================
    # 2. Carregar arquivo Parquet
    # =================================================
    df = pd.read_parquet(source)

    # =================================================
    # 3. Remover colunas auxiliares
    # =================================================
    columns_to_exclude = EXCLUDED_COLUMNS.get(
        source.stem,
        [],
    )

    df = df.drop(
        columns=columns_to_exclude,
        errors="ignore",
    )

    # =================================================
    # 4. Exportar CSV
    # =================================================
    df.to_csv(
        destination,
        index=False,
        sep="|",
        encoding="utf-8",
    )
