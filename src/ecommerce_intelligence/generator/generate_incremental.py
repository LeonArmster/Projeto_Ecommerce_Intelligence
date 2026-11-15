
# =====================================================
# Orquestração da geração incremental de dados
# =====================================================
# Bibliotecas
import logging
from time import perf_counter
from ecommerce_intelligence.generator import (
    generate_incremental_orders,
    generate_incremental_order_items,
    generate_incremental_payments,
    generate_incremental_shipments,
    generate_incremental_reviews,
)


LOGGER = logging.getLogger(__name__)


def main() -> None:
    """
    Executa a geração incremental dos dados de e-commerce.

    Os geradores são executados sequencialmente,
    respeitando as dependências entre as entidades.

    A execução preserva os registros históricos
    armazenados nos arquivos Parquet.

    Returns
    -------
    None
    """

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    # =================================================
    # 1. Configurar sequência de execução
    # =================================================
    generators = [
        ("Pedidos", generate_incremental_orders.main),
        ("Itens dos pedidos", generate_incremental_order_items.main),
        ("Pagamentos", generate_incremental_payments.main),
        ("Entregas", generate_incremental_shipments.main),
        ("Avaliações", generate_incremental_reviews.main),
    ]
    
    LOGGER.info("Iniciando geração incremental.")

    start_time = perf_counter()

    # =================================================
    # 2. Executar geradores
    # =================================================
    for name, generator in generators:

        LOGGER.info("Iniciando: %s", name)

        step_start = perf_counter()

        generator()

        LOGGER.info(
            "Concluído: %s | Tempo: %.2f segundos",
            name,
            perf_counter() - step_start,
        )

    # =================================================
    # 3. Finalizar processamento
    # =================================================
    LOGGER.info(
        "Geração incremental concluída | Tempo total: %.2f segundos",
        perf_counter() - start_time,
    )


if __name__ == "__main__":
    main()
