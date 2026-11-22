
import pytest
from jsonschema import ValidationError, validate

from ecommerce_intelligence.ai.schemas import (
    BUSINESS_BRIEF_SCHEMA,
)


def test_business_brief_valid_schema():
    brief = {
        "executive_summary": "Net sales increased.",
        "signals": [
            {
                "metric": "net_sales_change_pct",
                "description": "Sales increased by 3.5%.",
            }
        ],
        "attention_points": ["Monitor cancellations."],
        "investigations": ["Analyze sales by product category."],
    }

    validate(instance=brief, schema=BUSINESS_BRIEF_SCHEMA)


def test_business_brief_invalid_schema():
    brief = {
        "executive_summary": "Net sales increased.",
        "signals": [],
    }

    with pytest.raises(ValidationError):
        validate(instance=brief, schema=BUSINESS_BRIEF_SCHEMA)
