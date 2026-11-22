
import pytest

from ecommerce_intelligence.ai.business_rules import (
    classify_direction,
    classify_severity,
)


@pytest.mark.parametrize(
    "value, expected",
    [
        (10.0, "up"),
        (-5.0, "down"),
        (0.0, "stable"),
    ],
)
def test_classify_direction(value, expected):
    assert classify_direction(value) == expected


@pytest.mark.parametrize(
    "value, medium, high, expected",
    [
        (0.02, 0.05, 0.10, "low"),
        (0.05, 0.05, 0.10, "medium"),
        (0.10, 0.05, 0.10, "high"),
        (-0.10, 0.05, 0.10, "high"),
    ],
)
def test_classify_severity(value, medium, high, expected):
    result = classify_severity(
        value=value,
        medium_threshold=medium,
        high_threshold=high,
    )

    assert result == expected
