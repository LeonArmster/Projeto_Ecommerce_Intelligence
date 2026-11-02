INSERT INTO ai.business_briefs (
    reference_date,
    provider,
    model_name,
    context_data,
    brief_data,
    generation_duration_seconds
)
VALUES (
    %s,
    %s,
    %s,
    %s::jsonb,
    %s::jsonb,
    %s
)

ON CONFLICT (
    reference_date,
    provider,
    model_name
)

DO UPDATE SET
    context_data = EXCLUDED.context_data,
    brief_data = EXCLUDED.brief_data,
    generation_duration_seconds =
        EXCLUDED.generation_duration_seconds,
    generated_at = CURRENT_TIMESTAMP;