# Agent Memory

## Project: Model Training Loop

This is a personal AI assistant CLI built on LangChain DeepAgents with SQLite checkpointing.

## Key Files

- `cli/main.py` - Main CLI entry point
- `cli/analyze.py` - Conversation analysis CLI
- `agent/conversation_analyzer.py` - Analysis logic (reusable)
- `sessions/checkpoints.db` - SQLite database storing conversation checkpoints
- `analysis/` - Directory for analysis output

## User Preferences

- Prefers concise answers (4 lines or less unless detail is requested)

## Skills

This agent has access to skills in `.deepagents/skills/`:

- `conversation-analyzer/` - Analyze conversations for intent and quality
- `user-context-simulator/` - Manage 4-layer user context
- `conversation-simulator/` - Simulate conversations with bots via API
- `skill-author/` - How to create new skills

## User Context

User preferences stored in `user_context.json`:
- Physical: age, sex, notes
- Mental: mood, values, biases, likes, dislikes, experience
- User Context: bot-specific info (e.g., road_trip.car_type)
- Explicit Preferences: communication_style, response_length

## Available Tools

- `get_country_info` - Get country information (capital, population, languages, currency)
- Standard DeepAgents tools: read_file, write_file, ls, glob, grep, shell

## Data Sources

- Sessions stored in SQLite at `sessions/checkpoints.db`
- Each session has a thread_id
- Query sessions with: `SELECT * FROM checkpoints WHERE thread_id = 'xxx'`

## Analysis Output

Analysis results are saved to `analysis/chat_Analysis_{date}.json`
