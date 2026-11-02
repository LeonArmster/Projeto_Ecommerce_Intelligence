# ===========================================
# Criando o logger para observalidade
# ===========================================

import logging
import sys


def configure_logger() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
        handlers=[
            logging.StreamHandler(sys.stdout)
        ],
        force=True,
    )