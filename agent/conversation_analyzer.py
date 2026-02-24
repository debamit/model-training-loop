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
3. If existing goals are provided, decide which new conversations fit existing goals (>80% similar) and which need new goal entries

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


def get_session_date(session_id: str) -> Optional[str]:
    """Get the date of a session from checkpoint metadata (YYYY-MM-DD)."""
    import sqlite3

    conn = sqlite3.connect("sessions/checkpoints.db")
    cur = conn.cursor()
    cur.execute(
        "SELECT checkpoint_id FROM checkpoints WHERE thread_id = ? ORDER BY checkpoint_id ASC LIMIT 1",
        (session_id,),
    )
    row = cur.fetchone()
    conn.close()

    if row and row[0]:
        ckpt_id = row[0]
        timestamp_part = ckpt_id.split("-")[0]
        try:
            ts = int(timestamp_part, 16)
            dt = datetime.fromtimestamp(ts / 1000)
            return dt.strftime("%Y-%m-%d")
        except (ValueError, IndexError):
            pass

    return datetime.now().strftime("%Y-%m-%d")


def analyze_conversations(
    session_ids: list[str],
    model: Optional[object] = None,
    existing_goals: Optional[list[GoalGroup]] = None,
) -> AnalysisOutput:
    """Analyze conversations and group by goals.

    Args:
        session_ids: List of session IDs to analyze
        model: Chat model to use (default: from config)
        existing_goals: Existing goals to match against (for merging)
    """
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

    user_prompt_parts = []

    if existing_goals:
        existing_goals_json = json.dumps(
            [
                {
                    "goal": g.goal,
                    "conversation_ids": [c.conversation_id for c in g.conversations],
                }
                for g in existing_goals
            ],
            indent=2,
        )
        user_prompt_parts.append(
            f"EXISTING GOALS (use 80% similarity threshold to match new conversations to these goals):\n{existing_goals_json}"
        )

    user_prompt_parts.append(
        f"""NEW CONVERSATIONS TO ANALYZE:
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
    )

    user_prompt = (
        "Analyze these conversations and group them by goal. Output JSON:\n\n"
        + "\n\n".join(user_prompt_parts)
    )

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


def load_existing_analysis(
    date: str, output_dir: str = "./analysis"
) -> Optional[AnalysisOutput]:
    """Load existing analysis file for a given date."""
    from pathlib import Path

    filepath = Path(output_dir) / f"chat_Analysis_{date}.json"
    if not filepath.exists():
        return None

    with open(filepath) as f:
        data = json.load(f)

    goals = []
    for goal_data in data.get("goals", []):
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
        date=data.get("date", date),
        analyzed_at=data.get("analyzed_at", ""),
        source_sessions=data.get("source_sessions", []),
        goals=goals,
    )
