---
name: conversation-analyzer
description: Analyzes conversations to understand user intent and measure conversation quality. Classifies messages as Query (information seeking), Action (task execution), or Preference (context sharing). Measures sentiment (positive/neutral/negative/frustrated), urgency (high/exploratory), clarity (well-defined/ambiguous), and follow-up type (new topic/continuation).
trigger: analyze conversation, classify intent, measure quality, understand user feedback, sentiment analysis
---

# Conversation Analyzer

You analyze conversations between users and AI assistants to understand how the conversation flows and the quality of interaction.

## Intent Classification

Classify each user message into one of:

1. **Query** - Information seeking (questions, clarifications, exploring options)
2. **Action** - Task execution (requests to do something, commands)
3. **Preference** - Context sharing (opinions, constraints, feedback, background info)

## Quality Metrics

For each message/turn, measure:
- **Sentiment**: positive, neutral, negative, frustrated
- **Urgency**: high_priority, exploratory
- **Clarity**: well_defined, ambiguous, needs_clarification
- **Follow-up**: new_topic, continuation

## How to Analyze (DO THIS EXACTLY)

Run the existing CLI to get conversation data:

```bash
cd /home/debamit007/model-training-loop && python -c "
from agent.conversation_analyzer import get_session_messages
import json
msgs = get_session_messages('SESSION_ID')
for m in msgs:
    print(json.dumps(m))
"
```

Example for session `b7a8bfbd`:

```bash
cd /home/debamit007/model-training-loop && python -c "
from agent.conversation_analyzer import get_session_messages
import json
msgs = get_session_messages('b7a8bfbd')
for m in msgs:
    print(json.dumps(m))
"
```

This returns all messages. Then classify each user message (type='human') for intent and quality.

## Output Format

```json
{
  "conversation_id": "b7a8bfbd",
  "total_turns": 5,
  "intents": {"query": 3, "action": 1, "preference": 1},
  "quality": {"avg_sentiment": "neutral", "clarity_issues": 1, "follow_ups": 2},
  "turns": [
    {
      "turn": 1,
      "user_message": "I want to plan a trip to Japan",
      "intent": "action",
      "sentiment": "positive",
      "urgency": "exploratory",
      "clarity": "well_defined",
      "follow_up": "new_topic"
    }
  ]
}
```
