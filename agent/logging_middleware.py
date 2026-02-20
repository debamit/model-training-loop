from datetime import datetime, timezone
from langchain_core.tools import tool


class AgentLoggingTool:
    def __init__(self):
        self.current_goal_id = None
        self.current_journey_id = None

    def log_goal(self, user_intent: str, goal_type: str = "general") -> str:
        self.current_goal_id = f"goal_{int(datetime.now(timezone.utc).timestamp())}"
        self.current_journey_id = (
            f"journey_{int(datetime.now(timezone.utc).timestamp())}"
        )
        return f"Goal logged: {self.current_goal_id}, Journey started: {self.current_journey_id}"

    def log_step(
        self,
        step_type: str,
        description: str,
        tool_name: str | None = None,
        input_data: dict | None = None,
        output_data: dict | None = None,
    ) -> str:
        if not self.current_journey_id:
            return "No active journey. Call log_goal first."
        return f"Step logged: {step_type} - {description}"

    def complete_journey(self, status: str = "completed") -> str:
        if not self.current_journey_id:
            return "No active journey to complete."
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
    tool_name: str | None = None,
    input_data: dict | None = None,
    output_data: dict | None = None,
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
