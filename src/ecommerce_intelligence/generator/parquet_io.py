"""Shared Parquet writer for warehouse-compatible timestamps."""

from pathlib import Path

import pandas as pd


def save_parquet(df: pd.DataFrame, file_path: Path) -> None:
    """Write microsecond timestamps without silently losing precision."""
    df.to_parquet(
        file_path,
        engine="pyarrow",
        index=False,
        coerce_timestamps="us",
        allow_truncated_timestamps=False,
    )
