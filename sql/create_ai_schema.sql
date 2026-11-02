CREATE SCHEMA IF NOT EXISTS ai;

CREATE TABLE IF NOT EXISTS ai.business_briefs (
    brief_id BIGSERIAL PRIMARY KEY,

    reference_date DATE NOT NULL,

    provider VARCHAR(50) NOT NULL,
    model_name VARCHAR(100) NOT NULL,

    context_data JSONB NOT NULL,
    brief_data JSONB NOT NULL,

    generated_at TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (
        reference_date,
        provider,
        model_name
    )
);