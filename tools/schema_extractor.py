from typing import Any


def extract_schema(data: Any) -> dict:
    """Recursively extract JSON structure with types."""
    if data is None:
        return {"type": "null"}
    elif isinstance(data, bool):
        return {"type": "boolean"}
    elif isinstance(data, int):
        return {"type": "integer"}
    elif isinstance(data, float):
        return {"type": "number"}
    elif isinstance(data, str):
        return {"type": "string"}
    elif isinstance(data, list):
        if data:
            return {"type": "array", "items": extract_schema(data[0])}
        return {"type": "array"}
    elif isinstance(data, dict):
        return {
            "type": "object",
            "properties": {k: extract_schema(v) for k, v in data.items()},
        }
    return {"type": "unknown"}
