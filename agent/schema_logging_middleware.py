from typing import Any
from langchain.agents.middleware import AgentMiddleware
from tools.schema_extractor import extract_schema
from logger import AgentLogger


class SchemaLoggingMiddleware(AgentMiddleware):
    """Middleware to log tool call schemas to the journey."""

    def __init__(self, storage_path: str = "weights_n_biases.json"):
        self.storage_path = storage_path
        self.logger = AgentLogger(storage_path=storage_path)
        self.current_journey_id = None

    def wrap_tool_call(self, request, handler):
        tool_name = (
            request.tool_call.get("name")
            if hasattr(request, "tool_call")
            else str(request)
        )
        print(f"[SchemaLoggingMiddleware] Tool: {tool_name}")

        result = handler(request)

        print(f"[SchemaLoggingMiddleware] Result type: {type(result)}")
        print(f"[SchemaLoggingMiddleware] Result: {result}")

        schema = extract_schema(result)

        self._log_schema(tool_name, schema)

        return result

    def _log_schema(self, tool_name: str, schema: dict):
        storage = self._read_storage()
        journeys = storage.get("journeys", [])

        if journeys:
            current_journey = journeys[-1]
            journey_id = current_journey.get("id")

            if journey_id:
                step = {
                    "step_type": "tool_call",
                    "description": f"Tool: {tool_name}",
                    "timestamp": self._get_timestamp(),
                    "tool_name": tool_name,
                    "input_data": None,
                    "output_data": {"schema": schema},
                }
                current_journey["steps"].append(step)
                self._write_storage(storage)
                print(
                    f"[SchemaLoggingMiddleware] Logged schema to journey: {journey_id}"
                )

    def _read_storage(self):
        import json

        try:
            with open(self.storage_path, "r") as f:
                return json.load(f)
        except:
            return {"goals": [], "journeys": []}

    def _write_storage(self, data):
        import json

        with open(self.storage_path, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def _get_timestamp(self):
        from datetime import datetime, timezone

        return datetime.now(timezone.utc).isoformat()
