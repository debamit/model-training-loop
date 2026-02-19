import json
from datetime import datetime
from pathlib import Path
from schemas import Goal, Journey, JourneyStep


class AgentLogger:
    def __init__(self, storage_path: str = "weights_n_biases.json"):
        self.storage_path = Path(storage_path)
        self._ensure_storage_exists()

    def _ensure_storage_exists(self):
        if not self.storage_path.exists() or self.storage_path.read_text() == "":
            self.storage_path.write_text('{"goals": [], "journeys": []}')

    def _read_storage(self) -> dict:
        with open(self.storage_path, "r") as f:
            return json.load(f)

    def _write_storage(self, data: dict):
        with open(self.storage_path, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def log_goal(self, goal: Goal):
        storage = self._read_storage()
        storage["goals"].append(goal.model_dump())
        self._write_storage(storage)
        return goal.id

    def start_journey(self, goal_id: str, goal_type: str, goal_intent: str) -> str:
        storage = self._read_storage()
        journey = {
            "id": f"journey_{datetime.utcnow().timestamp()}",
            "goal_id": goal_id,
            "goal_type": goal_type,
            "goal_intent": goal_intent,
            "steps": [],
            "started_at": datetime.utcnow().isoformat(),
            "completed_at": None,
            "status": "in_progress",
        }
        storage["journeys"].append(journey)
        self._write_storage(storage)
        return journey["id"]

    def add_step(
        self,
        journey_id: str,
        step_type: str,
        description: str,
        tool_name: str = None,
        input_data: dict = None,
        output_data: dict = None,
    ):
        storage = self._read_storage()
        for journey in storage["journeys"]:
            if journey["id"] == journey_id:
                step = {
                    "step_type": step_type,
                    "description": description,
                    "timestamp": datetime.utcnow().isoformat(),
                    "tool_name": tool_name,
                    "input_data": input_data,
                    "output_data": output_data,
                }
                journey["steps"].append(step)
                break
        self._write_storage(storage)

    def complete_journey(self, journey_id: str, status: str = "completed"):
        storage = self._read_storage()
        for journey in storage["journeys"]:
            if journey["id"] == journey_id:
                journey["status"] = status
                journey["completed_at"] = datetime.utcnow().isoformat()
                break
        self._write_storage(storage)

    def get_journey(self, journey_id: str) -> dict:
        storage = self._read_storage()
        for journey in storage["journeys"]:
            if journey["id"] == journey_id:
                return journey
        return None

    def list_goals(self) -> list:
        storage = self._read_storage()
        return storage.get("goals", [])

    def list_journeys(self) -> list:
        storage = self._read_storage()
        return storage.get("journeys", [])
