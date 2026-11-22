# AI Business Intelligence Layer

## AI Business Intelligence Layer

The first AI capability of the platform is the **AI Business Brief**.

Its purpose is to transform validated business metrics into a concise executive interpretation.

The architecture deliberately separates deterministic computation from generative interpretation.

```text
dbt
 │
 ├── calculates metrics
 └── calculates variations
          │
          ▼
Business Context
          │
          ▼
Business Rules
 │
 ├── direction
 └── severity
          │
          ▼
LLM
 │
 ├── interpretation
 ├── synthesis
 └── investigation recommendations
          │
          ▼
Structured Output
```

The LLM does **not** calculate core business metrics.

Those calculations belong to the analytical platform.

---

## Business Context

The Business Context layer retrieves validated metrics from PostgreSQL and prepares them for AI consumption.

It contains three categories of information:

```text
context
│
├── metrics
│   ├── net_amount
│   ├── valid_orders
│   ├── delay_rate
│   └── ...
│
├── metadata
│   ├── analysis_granularity
│   └── comparison_type
│
└── deterministic signals
    └── metric_signals
        ├── direction
        └── severity
```

For V1:

```text
analysis_granularity = daily
comparison_type = previous_day
```

This prevents the LLM from incorrectly inferring temporal granularity.

---

## Deterministic Business Rules

Not every analytical decision should be delegated to an LLM.

Metric direction and severity are calculated deterministically in Python.

Example:

```json
{
  "metric": "delay_rate_change_pp",
  "value": -2.83,
  "direction": "down",
  "severity": "medium"
}
```

This design provides reproducibility.

The same metric variation always produces the same classification regardless of which LLM is being used.

The LLM is responsible for **interpretation**, not deterministic classification.

---

## Local LLM with Ollama

The project uses **Ollama** as the local LLM runtime.

Current model:

```text
Qwen3 8B
```

Benefits of local inference for this project include:

- no API inference cost;
- local experimentation;
- data remains within the local environment;
- provider-independent architecture;
- GPU acceleration.

The development machine can use an NVIDIA GPU for local inference.

The architecture does not depend directly on Ollama.

Instead, the application uses an LLM provider abstraction.

```text
Business Brief
      │
      ▼
LLMProvider
      │
      ├── Ollama
      │
      ├── Future Databricks Provider
      │
      └── Future Cloud Provider
```

This makes the AI layer replaceable without changing the analytical pipeline.

---

## Docker to Ollama Communication

Airflow runs inside Docker while Ollama runs on the host machine.

The communication path is:

```text
Airflow Container
       │
       ▼
host.docker.internal
       │
       ▼
Host Machine
       │
       ▼
Ollama :11434
       │
       ▼
Qwen3 8B
```

Docker Compose maps the host gateway so containers can resolve:

```text
host.docker.internal
```

The Ollama endpoint used by Airflow is therefore:

```text
http://host.docker.internal:11434
```

while local Python development can use:

```text
http://localhost:11434
```

The application code remains unchanged because the endpoint is controlled through environment variables.

---

## Structured AI Output

The AI does not return arbitrary free-form text.

A JSON Schema defines the expected response contract.

Conceptually:

```json
{
  "executive_summary": "...",
  "signals": [
    {
      "metric": "delay_rate_change_pp",
      "description": "..."
    }
  ],
  "attention_points": [
    "..."
  ],
  "investigations": [
    "..."
  ]
}
```

Structured output makes AI responses usable by software rather than only readable by humans.

The result can therefore be:

- stored in PostgreSQL;
- exposed through an API;
- displayed in a dashboard;
- consumed by another application;
- compared across different LLM providers.

---

## AI Guardrails

The Business Brief prompt follows explicit analytical constraints.

The model must:

- use only provided indicators;
- avoid recalculating validated metrics;
- avoid inventing information;
- avoid unsupported causal claims;
- distinguish facts from hypotheses;
- respect percentage and percentage-point semantics;
- respect the provided temporal granularity;
- recommend investigations rather than invent conclusions.

For example, instead of claiming:

> Delivery performance improved because the logistics team implemented a new process.

the expected behavior is:

> Delivery performance improved compared with the previous period. The available indicators do not identify the cause of this change, so additional investigation is required.

This distinction is fundamental to the AI architecture of the project.

---

## AI Persistence and Traceability

Generated Business Briefs are stored in PostgreSQL.

The `ai.business_briefs` table stores:

```text
reference_date
provider
model_name
context_data
brief_data
generation_duration_seconds
generated_at
```

Both the analytical context and AI output are stored as JSONB.

This provides traceability:

```text
Which data was used?
        │
        ▼
Which business rules were applied?
        │
        ▼
Which provider generated the result?
        │
        ▼
Which model was used?
        │
        ▼
What output was generated?
```

This architecture also makes future model comparisons possible.

---

## Idempotency

AI persistence is designed to support retries safely.

The logical key is:

```text
reference_date
+
provider
+
model_name
```

The PostgreSQL persistence layer uses an UPSERT strategy.

Therefore, retrying the same execution updates the existing Business Brief instead of creating duplicate records.

This is especially important when the AI task runs under Airflow retry policies.

---
