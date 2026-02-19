import os
import tempfile
from datetime import datetime
from logger import AgentLogger
from schemas import Goal, GoalType


def test_logger_basic():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as f:
        path = f.name

    try:
        logger = AgentLogger(storage_path=path)

        goal = Goal(
            id="goal_1",
            user_intent="Pay my credit card bill",
            goal_type=GoalType.PAYMENT,
            created_at=datetime.utcnow(),
            constraints=[],
            metadata={},
        )
        goal_id = logger.log_goal(goal)

        assert goal_id == "goal_1"

        journey_id = logger.start_journey(
            goal_id=goal_id, goal_type="payment", goal_intent="Pay my credit card bill"
        )

        assert journey_id.startswith("journey_")

        logger.add_step(
            journey_id=journey_id,
            step_type="user_input",
            description="User requested payment",
        )

        logger.complete_journey(journey_id)

        journey = logger.get_journey(journey_id)
        assert journey["status"] == "completed"
        assert len(journey["steps"]) == 1

        goals = logger.list_goals()
        assert len(goals) == 1

        print("All tests passed!")

    finally:
        os.unlink(path)


if __name__ == "__main__":
    test_logger_basic()
