# MVP 002 - Conversation Analysis Agent

## Overview

Analyze conversations from SQLite, group by goals, output to `chat_Analysis_{date}.json`.

## Input

### CLI Interface

```bash
# Analyze single conversation
python -m cli.analyze <conversation_id>

# Analyze all conversations from a day
python -m cli.analyze --day 2026-02-23

# List available session IDs
python -m cli.analyze --list
```

### Default Options
- Output directory: `./analysis/` (configurable via `--output-dir`)
- Overwrites existing files for same date

---

## Output

### File Structure

```
analysis/
├── chat_Analysis_2026-02-23.json
├── chat_Analysis_2026-02-24.json
└── ...
```

### JSON Schema

```json
{
  "date": "2026-02-23",
  "analyzed_at": "2026-02-23T14:30:00Z",
  "source_sessions": ["session_001", "session_002"],
  "goals": [
    {
      "goal": "road trip",
      "conversations": [
        {
          "conversation_id": "session_001",
          "steps": [
            {
              "type": "tool_call",
              "tool": "web_search",
              "input": "road trip LA to NY scenic route",
              "output": "..."
            },
            {
              "type": "reasoning",
              "content": "User wants scenic route so prioritizing national parks route..."
            },
            {
              "type": "final_answer",
              "content": "Here's your 5-day road trip plan..."
            }
          ],
          "tools_used": ["web_search", "get_country_info"],
          "sources_checked": ["nps.gov", "wikipedia"],
          "user_preference": "prefer scenic routes",
          "user_context": "user location: LA"
        }
      ]
    }
  ]
}
```

---

## LLM Prompt for Grouping

```
You are analyzing conversations between a user and AI assistant.

Group conversations by GOAL. A goal represents what the user was trying to accomplish.

Rules:
1. If user_intent is >80% semantically similar to an existing goal, add to that goal group
2. Eg: "plan a road trip" and "trip from LA to NY" = same goal
3. Eg: "book flight" and "research hotels" = different goals
4. If conversation has multiple distinct goals, split into separate goal entries

For each conversation, extract:
- steps: tool calls made, reasoning, final answer
- tools_used: list of tools invoked
- sources_checked: URLs/data sources used
- user_preference: any preferences revealed
- user_context: any context provided (location, payment info, etc)
```

---

## Implementation

### Files to Create/Modify

```
cli/
└── analyze.py              # CLI entry point

agent/
└── conversation_analyzer.py # LLM-based analysis

schemas/
└── analysis.py             # Pydantic models
```

### Dependencies
- Existing: `deepagents`, `langgraph`, `sqlite`
- New: None required
