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

                    "direction": {
                        "type": "string",
                        "enum": [
                            "up",
                            "down",
                            "stable"
                        ]
                    },

                    "severity": {
                        "type": "string",
                        "enum": [
                            "low",
                            "medium",
                            "high"
                        ]
                    },

                    "description": {
                        "type": "string"
                    },
                },

                "required": [
                    "metric",
                    "direction",
                    "severity",
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