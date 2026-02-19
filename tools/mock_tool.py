from schemas import GoalType


class MockTool:
    RESPONSES = {
        GoalType.PAYMENT.value: "I've processed your credit card payment. Amount: $XXX, Date: Today, Confirmation: #ABC123",
        GoalType.TRAVEL.value: "Here's your travel itinerary:\n- Destination: [TBD based on query]\n- Departure: [TBD]\n- Return: [TBD]\n\nNote: This is a mock response for testing.",
        GoalType.RESEARCH.value: "Research Summary:\n\nBased on available information, I found the following:\n[Your query would be processed here]\n\nNote: This is a mock response for testing.",
        GoalType.GENERAL.value: "I've processed your request: '{query}'\n\nNote: This is a mock response for testing.",
    }

    def execute(self, goal_type: str, context: dict = None) -> dict:
        response = self.RESPONSES.get(goal_type, self.RESPONSES[GoalType.GENERAL.value])

        if "{query}" in response and context:
            response = response.format(query=context.get("query", ""))

        return {"response": response, "tool_name": "MockTool", "status": "success"}
