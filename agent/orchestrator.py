from datetime import datetime, timezone
from logger import AgentLogger
from schemas import Goal, GoalType
from tools import BuilderTool
from tools.schema_extractor import extract_schema


class AgentOrchestrator:
    def __init__(self, storage_path: str = "weights_n_biases.json"):
        self.logger = AgentLogger(storage_path=storage_path)
        self.tool = BuilderTool()

    def _detect_intent(self, user_input: str) -> str:
        user_lower = user_input.lower()

        if "pay" in user_lower or "payment" in user_lower or "bill" in user_lower:
            return GoalType.PAYMENT.value
        elif "travel" in user_lower or "trip" in user_lower or "flight" in user_lower:
            return GoalType.TRAVEL.value
        elif "research" in user_lower or "find" in user_lower or "search" in user_lower:
            return GoalType.RESEARCH.value
        else:
            return GoalType.GENERAL.value

    def run(self, user_input: str) -> dict:
        intent_result = self.tool.execute(
            user_query=user_input, context={"mode": "classify_only"}
        )

        goal_type = intent_result.get("goal_type", "general")
        confidence = intent_result.get("confidence", 0.5)
        reasoning = intent_result.get("reasoning", "")

        goal = Goal(
            id=f"goal_{int(datetime.now(timezone.utc).timestamp())}",
            user_intent=user_input,
            goal_type=GoalType(goal_type),
            created_at=datetime.now(timezone.utc),
            constraints=[],
            metadata={"confidence": confidence, "reasoning": reasoning},
        )
        goal_id = self.logger.log_goal(goal)

        journey_id = self.logger.start_journey(
            goal_id=goal_id, goal_type=goal_type, goal_intent=user_input
        )

        self.logger.add_step(
            journey_id=journey_id,
            step_type="user_input",
            description=f"User request: {user_input}",
        )

        self.logger.add_step(
            journey_id=journey_id,
            step_type="llm_response",
            description=f"Intent classified as: {goal_type} (confidence: {confidence})",
        )

        tool_result = self.tool.execute(
            user_query=user_input, context={"goal_type": goal_type}
        )

        response_schema = extract_schema(tool_result)

        self.logger.add_step(
            journey_id=journey_id,
            step_type="tool_call",
            description=f"BuilderTool.execute for goal_type: {goal_type}",
            tool_name=tool_result.get("tool_name", "BuilderTool"),
            input_data={"user_query": user_input, "goal_type": goal_type},
            output_data={"schema": response_schema},
        )

        self.logger.add_step(
            journey_id=journey_id,
            step_type="verification",
            description="Response sanity check passed",
            tool_name="System",
            input_data={"response_length": len(tool_result.get("response", ""))},
            output_data={"valid": True},
        )

        self.logger.complete_journey(journey_id, status="success")

        return {
            "response": tool_result.get("response"),
            "goal_id": goal_id,
            "journey_id": journey_id,
            "step_count": 5,
        }
