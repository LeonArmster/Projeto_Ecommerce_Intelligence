import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from ecommerce_intelligence.generator.parquet_io import save_parquet


def test_microsecond_timestamp_roundtrip(tmp_path):
    path = tmp_path / "test.parquet"
    df = pd.DataFrame({
        "created_at": pd.Series(
            [pd.Timestamp("2026-01-01 12:00:00.123456"), pd.NaT],
            dtype="datetime64[ns]",
        ),
        "id": [1, 2],
    })
    save_parquet(df, path)
    table = pq.read_table(path)
    assert table.schema.field("created_at").type == pa.timestamp("us")
    assert table.column("created_at").to_pylist() == [
        df.loc[0, "created_at"].to_pydatetime(), None
    ]
    assert table.column("id").to_pylist() == [1, 2]


def test_reject_submicrosecond_precision(tmp_path):
    df = pd.DataFrame({
        "created_at": pd.Series(
            [pd.Timestamp("2026-01-01 12:00:00.123456789")],
            dtype="datetime64[ns]",
        ),
    })
    with pytest.raises(pa.ArrowInvalid):
        save_parquet(df, tmp_path / "invalid.parquet")
