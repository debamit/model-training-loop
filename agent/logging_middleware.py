from datetime import datetime, timezone
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from logger import AgentLogger
from schemas import Goal, GoalType

storage_path = "weights_n_biases.json"


class AgentLoggingTool:
    def __init__(self):
        self.logger = AgentLogger(storage_path=storage_path)
        self.current_goal_id = None
        self.current_journey_id = None

    def log_goal(self, user_intent: str, goal_type: str = "general") -> str:
        goal_id = f"goal_{int(datetime.now(timezone.utc).timestamp())}"

        try:
            goal_enum = GoalType(goal_type)
        except ValueError:
            goal_enum = GoalType.GENERAL

        goal = Goal(
            id=goal_id,
            user_intent=user_intent,
            goal_type=goal_enum,
            created_at=datetime.now(timezone.utc),
            constraints=[],
            metadata={},
        )

        self.current_goal_id = self.logger.log_goal(goal)

        self.current_journey_id = self.logger.start_journey(
            goal_id=self.current_goal_id, goal_type=goal_type, goal_intent=user_intent
        )

        return f"Goal logged: {goal_id}, Journey started: {self.current_journey_id}"

    def log_step(
        self,
        step_type: str,
        description: str,
        tool_name: str = None,
        input_data: dict = None,
        output_data: dict = None,
    ) -> str:
        if not self.current_journey_id:
            return "No active journey. Call log_goal first."

        self.logger.add_step(
            journey_id=self.current_journey_id,
            step_type=step_type,
            description=description,
            tool_name=tool_name,
            input_data=input_data,
            output_data=output_data,
        )

        return f"Step logged to journey: {self.current_journey_id}"

    def complete_journey(self, status: str = "completed") -> str:
        if not self.current_journey_id:
            return "No active journey to complete."

        self.logger.complete_journey(self.current_journey_id, status)
        result = f"Journey {self.current_journey_id} marked as {status}"
        self.current_goal_id = None
        self.current_journey_id = None
        return result

    def get_current_session(self) -> dict:
        return {
            "goal_id": self.current_goal_id,
            "journey_id": self.current_journey_id,
        }


logging_tool_instance = AgentLoggingTool()


@tool
def log_goal(user_intent: str, goal_type: str = "general") -> str:
    """Log a new user goal and start a journey. Always call this first when the user makes a request.

    Args:
        user_intent: The user's request or what they want to accomplish
        goal_type: Type of goal - payment, travel, research, or general
    """
    return logging_tool_instance.log_goal(user_intent, goal_type)


@tool
def log_step(
    step_type: str,
    description: str,
    tool_name: str = None,
    input_data: dict = None,
    output_data: dict = None,
) -> str:
    """Log a step in the current journey to track progress.

    Args:
        step_type: Type of step - user_input, assistant_response, tool_call, verification
        description: Description of what happened
        tool_name: Name of tool used if any
        input_data: Input data to the step
        output_data: Output data from the step
    """
    return logging_tool_instance.log_step(
        step_type, description, tool_name, input_data, output_data
    )


@tool
def complete_journey(status: str = "completed") -> str:
    """Complete the current journey when done helping the user.

    Args:
        status: completion status - completed, failed, or interrupted
    """
    return logging_tool_instance.complete_journey(status)


@tool
def get_current_session() -> dict:
    """Get the current session's goal and journey IDs for debugging."""
    return logging_tool_instance.get_current_session()
