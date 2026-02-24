import json
from datetime import datetime
from typing import Optional

from langgraph.checkpoint.sqlite import SqliteSaver

from config import create_chat_model
from schemas.analysis import AnalysisOutput, GoalGroup, ConversationEntry, Step


ANALYSIS_SYSTEM_PROMPT = """You are analyzing conversations between a user and AI assistant.

Group conversations by GOAL. A goal represents what the user was trying to accomplish.

Rules:
1. If user_intent is >80% semantically similar to an existing goal, add to that goal group
   Eg: "plan a road trip" and "trip from LA to NY" = same goal
   Eg: "book flight" and "research hotels" = different goals
2. If conversation has multiple distinct goals, split into separate goal entries

For each conversation, extract:
- steps: tool calls made, reasoning steps, final answer
- tools_used: list of tools invoked
- sources_checked: URLs/data sources used
- user_preference: any preferences revealed in the conversation
- user_context: any context provided (location, payment info, etc)

Output ONLY valid JSON, no markdown formatting or explanation."""


def format_message(msg) -> dict:
    """Format a message for analysis."""
    result = {
        "type": msg.type if hasattr(msg, "type") else "unknown",
        "content": msg.content if hasattr(msg, "content") else str(msg),
    }

    if hasattr(msg, "tool_calls") and msg.tool_calls:
        result["tool_calls"] = []
        for tc in msg.tool_calls:
            tc_dict = {
                "name": tc.get("name", tc.get("function", {}).get("name", "unknown")),
                "args": tc.get("args", tc.get("function", {}).get("arguments", "")),
            }
            result["tool_calls"].append(tc_dict)

    if hasattr(msg, "name") and msg.name:
        result["tool_name"] = msg.name

    return result


def get_session_messages(session_id: str) -> list[dict]:
    """Get all messages from a session."""
    with SqliteSaver.from_conn_string("sessions/checkpoints.db") as checkpointer:
        config = {"configurable": {"thread_id": session_id}}
        state = checkpointer.get(config)

        if not state or "channel_values" not in state:
            return []

        messages = state["channel_values"].get("messages", [])
        return [format_message(msg) for msg in messages]


def get_sessions_by_day(date: str) -> list[str]:
    """Get all session IDs for a given date (YYYY-MM-DD)."""
    with SqliteSaver.from_conn_string("sessions/checkpoints.db") as checkpointer:
        with checkpointer.cursor() as cur:
            cur.execute("SELECT DISTINCT thread_id FROM checkpoints")
            threads = [r[0] for r in cur.fetchall()]

    return threads


def get_all_sessions() -> list[str]:
    """Get all session IDs."""
    with SqliteSaver.from_conn_string("sessions/checkpoints.db") as checkpointer:
        with checkpointer.cursor() as cur:
            cur.execute("SELECT DISTINCT thread_id FROM checkpoints")
            threads = [r[0] for r in cur.fetchall()]

    return threads


def analyze_conversations(
    session_ids: list[str],
    model: Optional[object] = None,
) -> AnalysisOutput:
    """Analyze conversations and group by goals."""
    if model is None:
        model = create_chat_model()

    conversations_data = []
    for session_id in session_ids:
        messages = get_session_messages(session_id)
        if messages:
            conversations_data.append(
                {
                    "conversation_id": session_id,
                    "messages": messages,
                }
            )

    if not conversations_data:
        return AnalysisOutput(
            date=datetime.now().strftime("%Y-%m-%d"),
            analyzed_at=datetime.now().isoformat(),
            source_sessions=[],
            goals=[],
        )

    user_prompt = f"""Analyze these conversations and group them by goal. Output JSON:

conversations:
{json.dumps(conversations_data, indent=2)}

Output format:
{{
  "goals": [
    {{
      "goal": "goal description",
      "conversations": [
        {{
          "conversation_id": "session_id",
          "steps": [
            {{"type": "tool_call", "tool": "tool_name", "input": "...", "output": "..."}},
            {{"type": "reasoning", "content": "..."}},
            {{"type": "final_answer", "content": "..."}}
          ],
          "tools_used": ["tool1", "tool2"],
          "sources_checked": ["url1"],
          "user_preference": "...",
          "user_context": "..."
        }}
      ]
    }}
  ]
}}"""

    response = model.invoke(
        [
            {"role": "system", "content": ANALYSIS_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]
    )

    content = response.content if hasattr(response, "content") else str(response)

    if isinstance(content, list):
        for item in content:
            if item.get("type") == "text":
                content = item.get("text", "")
                break

    try:
        result = json.loads(content)
    except json.JSONDecodeError:
        import re

        json_match = re.search(r"\{[\s\S]*\}", content)
        if json_match:
            result = json.loads(json_match.group())
        else:
            result = {"goals": []}

    goals = []
    for goal_data in result.get("goals", []):
        conversations = []
        for conv in goal_data.get("conversations", []):
            steps = []
            for step in conv.get("steps", []):
                step_input = step.get("input")
                if isinstance(step_input, dict):
                    step_input = json.dumps(step_input)
                step_output = step.get("output")
                if isinstance(step_output, dict):
                    step_output = json.dumps(step_output)

                steps.append(
                    Step(
                        type=step.get("type", "unknown"),
                        tool=step.get("tool"),
                        input=step_input,
                        output=step_output,
                        content=step.get("content"),
                    )
                )

            conversations.append(
                ConversationEntry(
                    conversation_id=conv.get("conversation_id", ""),
                    steps=steps,
                    tools_used=conv.get("tools_used", []),
                    sources_checked=conv.get("sources_checked", []),
                    user_preference=conv.get("user_preference", ""),
                    user_context=conv.get("user_context", ""),
                )
            )

        goals.append(
            GoalGroup(
                goal=goal_data.get("goal", ""),
                conversations=conversations,
            )
        )

    return AnalysisOutput(
        date=datetime.now().strftime("%Y-%m-%d"),
        analyzed_at=datetime.now().isoformat(),
        source_sessions=session_ids,
        goals=goals,
    )
