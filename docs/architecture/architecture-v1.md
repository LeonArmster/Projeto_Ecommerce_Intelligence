flowchart TB

    %% =====================================================
    %% DATA SOURCE
    %% =====================================================

    subgraph SOURCE["Data Source"]
        A["Synthetic Data<br/>Python + Faker"]
        B["Parquet Storage"]

        A --> B
    end

    %% =====================================================
    %% DATA STORAGE
    %% =====================================================

    subgraph RAW["Data Storage"]
        C[("PostgreSQL<br/>RAW Layer")]
    end

    B --> C

    %% =====================================================
    %% ANALYTICS ENGINEERING
    %% =====================================================

    subgraph DBT["Analytics Engineering — dbt"]
        D["Staging"]
        E["Intermediate"]
        F["Marts"]
        G["Tests & Snapshots"]

        D --> E
        E --> F
        G -. "Data Quality & History" .-> D
        G -.-> E
        G -.-> F
    end

    C --> D

    %% =====================================================
    %% ANALYTICS LAYER
    %% =====================================================

    H[("PostgreSQL<br/>Analytics Layer")]

    F --> H

    %% =====================================================
    %% AI INTELLIGENCE
    %% =====================================================

    subgraph AI["AI Intelligence"]
        I["Business Context"]
        J["Business Rules<br/>Deterministic Classification"]
        K["Ollama<br/>Qwen3 8B<br/>Local GPU Inference"]
        L["Structured Output<br/>JSON Schema"]

        I --> J
        J --> K
        K --> L
    end

    H --> I

    %% =====================================================
    %% AI PERSISTENCE
    %% =====================================================

    M[("PostgreSQL<br/>AI Business Briefs")]

    L --> M

    %% =====================================================
    %% ORCHESTRATION
    %% =====================================================

    N["Apache Airflow<br/>Pipeline Orchestration"]

    N -. "Ingestion" .-> A
    N -. "Transformation" .-> D
    N -. "AI Generation" .-> I

    %% =====================================================
    %% INFRASTRUCTURE
    %% =====================================================

    O["Docker Compose<br/>Infrastructure & Networking"]

    O -.-> C
    O -.-> H
    O -.-> N