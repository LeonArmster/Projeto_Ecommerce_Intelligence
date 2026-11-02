BUSINESS_BRIEF_SCHEMA = {
    "type": "object",
    "properties": {

        "executive_summary": {
            "type": "string"
        },

    "signals": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {

                "metric": {
                    "type": "string"
                },

                "description": {
                    "type": "string"
                },
            },

            "required": [
                "metric",
                "description",
            ],
        },
    },
            "attention_points": {
                "type": "array",
                "items": {
                    "type": "string"
                },
            },

            "investigations": {
                "type": "array",
                "items": {
                    "type": "string"
                },
            },
        },

    "required": [
        "executive_summary",
        "signals",
        "attention_points",
        "investigations",
    ],
}