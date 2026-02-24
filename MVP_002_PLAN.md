# MVP 002 - Goal/Journey Extractor

## Overview

Extract Goals and Journeys from conversation history. This is a prerequisite for the Explorer Agent - it creates the data analyzed_conversation that the Explorer will analyze and improve.

## Single-Stage Pipeline

```
Conversation → chat_Analysis_{date}.json (intermediate)
```

### Stage 1: Extract (this MVP)
- Input: conversation.json OR --session-id (from SQLite)
- Output:  Analysis file
- LLM analyzes conversation, extracts goals/journeys


---

## Input

### CLI Interface

```bash
# From exported conversation.json
python -m cli.extract-goals conversation.json

# From session ID (SQLite)
python -m cli.extract-goals --session-id <SESSION_ID>

# With custom output directory
python -m cli.extract-goals conversation.json --output-dir ./my_goals
```

---

## Output

### File Structure

```
chat_Analysis_2026-02-23.json 
```

## chat_Analysis_{date}.json

Here have the goals and journeys extracted be seperated from the user preference and user context.

```json
{
  "analysis_date": "2026-02-23T10:00:00Z",
  "source_type": "conversation_file | session_id",
  "source_id": "conversation.json | session_xxx",
  "goals_extracted": [
    {
      "user_intent": "Plan a road trip from LA to NY",
      "category": "personal",
      "domain": "travel",
      "constraints": ["budget: $500", "timeframe: 5 days"],
      "user_preferences": ["prefer scenic routes", "likes national parks"],
      "matching_decision": "new_goal",
      "similarity_score": null,
      "reasoning": "User is planning a personal travel trip, no existing travel goal found",
      "journeys": [
        {
          "conversation_id": "session_xxx",
          "timestamp": "2026-02-23T10:00:00Z",
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
          "sources_checked": ["nps.gov", "wikipedia"]
        }
      ]
    }
  ]
}
```

---


---

## Extraction Logic (LLM-based)

### Static Prompt Instructions

```
You are analyzing a conversation between a user and AI assistant.

1. Identify the user's goal(s) - what were they trying to accomplish?
2. Extract any constraints/preferences they mentioned
3. Document the journey: tool calls made, reasoning steps, final answer
4. Decide: Does this match an existing goal (semantic similarity >80%)?
   If yes, append as new journey. If no, create new goal.
5. Classify as 'personal' or 'work' based on conversation context
6. Extract domain: travel, payment, research, or general
```

### Matching Logic

- **Threshold**: 80% semantic similarity
- **If score >= 80%**: Append journey to existing goal
- **If score < 80%**: Create new goal (auto-increment ID)

---

## What's Included in Journey

For each conversation, extract:

1. **Final answer** - The assistant's response
2. **Tool calls** - All tools invoked (name, input, output)
3. **Reasoning steps** - LLM's chain-of-thought (if available)
4. **User constraints** - Budget, timeline, requirements
5. **User preferences** - Likes, dislikes, priorities
6. **User context** - Their identity , their philosophy or other relevant context
7. **Sources checked** - URLs, APIs, data sources used


---

## Philosophy

- **On-demand + Scheduled**: User triggers manually, or can be run on schedule
- **Audit trail**: Keep intermediate analysis file for debugging
- **Extensible**: Static prompt can be tweaked later
- **Transparent**: Include LLM reasoning in intermediate output
