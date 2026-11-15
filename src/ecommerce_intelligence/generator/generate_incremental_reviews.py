# =====================================================
# Gerador incremental de dados = Avaliações
# =====================================================
# Bibliotecas
import logging
import os

import pandas as pd

from ecommerce_intelligence.config.config import raw_dir

from ecommerce_intelligence.generator.reviews import (
    generate_daily_reviews,
)

from ecommerce_intelligence.generator.generation_dates import (
    get_reference_date,
)


LOGGER = logging.getLogger(__name__)


def main() -> None:
    """Gera avaliações elegíveis para entregas concluídas, sem duplicar pedidos."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    # =================================================
    # 1. Carregar dados e definir data de referência
    # =================================================
    shipments_path = raw_dir / "shipments.parquet"
    reviews_path = raw_dir / "reviews.parquet"

    shipments = pd.read_parquet(shipments_path)
    reviews = pd.read_parquet(reviews_path)

    reference_date = get_reference_date()

    # =================================================
    # 2. Identificar entregas elegíveis
    # =================================================
    eligible_shipments = shipments[
        ~shipments["order_id"].isin(reviews["order_id"])
        & shipments["delivered_at"].notna()
    ].copy()

    LOGGER.info(
        "Entregas concluídas sem avaliação: %s",
        f"{len(eligible_shipments):,}",
    )

    # =================================================
    # 3. Gerar avaliações até a data de referência
    # =================================================
    new_reviews = generate_daily_reviews(
        shipments=eligible_shipments,
        reference_date=reference_date,
    )

    # =================================================
    # 4. Continuar sequência de IDs
    # =================================================
    if not new_reviews.empty:

        next_review_id = (
            int(reviews["review_id"].max()) + 1
            if not reviews.empty
            else 1
        )

        new_reviews.insert(
            0,
            "review_id",
            range(
                next_review_id,
                next_review_id + len(new_reviews),
            ),
        )

    else:
        new_reviews = pd.DataFrame(
            columns=reviews.columns
        )

    # =================================================
    # 5. Consolidar histórico e validar IDs
    # =================================================
    LOGGER.info(
        "Colunas histórico: %s",
        reviews.columns.tolist(),
    )

    LOGGER.info(
        "Colunas incremental: %s",
        new_reviews.columns.tolist(),
    )

    LOGGER.info(
        "Tipos histórico:\n%s",
        reviews.dtypes.to_string(),
    )

    LOGGER.info(
        "Tipos incremental:\n%s",
        new_reviews.dtypes.to_string(),
    )

    for column in reviews.columns.intersection(new_reviews.columns):

        historical_dtype = reviews[column].dtype
        incremental_dtype = new_reviews[column].dtype

        if (
            pd.api.types.is_datetime64_any_dtype(historical_dtype)
            or pd.api.types.is_datetime64_any_dtype(incremental_dtype)
        ):
            reviews[column] = pd.to_datetime(
                reviews[column]
            ).astype("datetime64[ns]")

            new_reviews[column] = pd.to_datetime(
                new_reviews[column]
            ).astype("datetime64[ns]")

            LOGGER.info(
                "Coluna temporal padronizada: %s",
                column,
            )

    updated = pd.concat(
        [reviews, new_reviews],
        ignore_index=True,
    )

    # Impede duplicações antes de persistir os registros.
    if updated["review_id"].duplicated().any():
        raise ValueError(
            "review_id duplicado."
        )

    if updated["order_id"].duplicated().any():
        raise ValueError(
            "Pedido com mais de uma avaliação."
        )

    # =================================================
    # 6. Salvar Parquet com substituição segura
    # =================================================
    temp_path = reviews_path.with_suffix(".tmp.parquet")

    # O arquivo temporário evita substituir o histórico antes da gravação.
    try:
        updated.to_parquet(
            temp_path,
            index=False,
        )

        os.replace(temp_path, reviews_path)

    finally:
        if temp_path.exists():
            temp_path.unlink()

    LOGGER.info(
        "Novas avaliações: %s",
        f"{len(new_reviews):,}",
    )

    LOGGER.info(
        "Total de avaliações: %s",
        f"{len(updated):,}",
    )

    LOGGER.info(
        "Geração incremental de avaliações concluída."
    )


if __name__ == "__main__":
    main()
