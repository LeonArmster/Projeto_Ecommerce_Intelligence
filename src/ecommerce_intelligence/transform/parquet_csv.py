# ============================================
# Arquivo de conversão de parquet para csv
# ============================================
# Bibliotecas
from pathlib import Path
import pandas as pd


def parquet_to_csv(
    source: Path,
    destination: Path,
) -> None:
    """
    Converte um arquivo Parquet para CSV
    utilizado na carga do PostgreSQL.
    """

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df = pd.read_parquet(source)

    df.to_csv(
        destination,
        index=False,
        sep="|",
        encoding="utf-8",
    )