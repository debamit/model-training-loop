# MVP 001 - Explorer Agent

## Overview

The Explorer Agent analyzes conversation history from the DeepAgent and manages user goals/journeys with persistent storage.

## Input/Output

- **Input**: Reads from `conversation.json` (auto-exported from DeepAgent sessions)
- **Output**:
  - `goals/goal_XXX.json` - One file per goal, contains goal + journeys array
  - `reports/YYYY-MM-DD_report.md` - Markdown report with analysis and recommendations

## File Structure

```
/explorer/
├── goals/
│   ├── goal_001.json    # Goal + journeys array
│   └── goal_002.json
├── reports/
│   └── 2026-02-19_analysis.md
└── agent.py             # Explorer agent definition
```

## Goal/Journey Model

Each goal file contains:

```json
{
  "id": "goal_001",
  "user_intent": "Go from LA to NY",
  "goal_type": "travel",
  "journeys": [
    {
      "id": "journey_001",
      "option_name": "Road trip",
      "tradeoffs": "Time: 40h, Cost: $300 gas, Experience: scenic",
      "steps": [...]
    },
    {
      "id": "journey_002", 
      "option_name": "Flight",
      "tradeoffs": "Time: 5h, Cost: $200+, Experience: efficient",
      "steps": [...]
    }
  ]
}
```

## Behavior

1. **On-demand**: User triggers via CLI: `python -m cli.explorer <conversation.json>`
2. **Analysis**: Reads conversation.json, uses LLM to analyze
3. **Matching**: LLM decides whether to create new goal or update existing (semantic matching)
4. **Research**: Uses tools to gather more info, generates recommendations
5. **Output**: Creates/updates goal files, generates markdown report

## CLI Interface

```bash
# Analyze a conversation file
python -m cli.explorer conversation.json

# With custom output directory
python -m cli.explorer conversation.json --output-dir ./my_goals
```

## Explorer Tools

- Read/write files
- Web search
- Custom research tools (TBD)

## Philosophy

- **Goal**: The objective (e.g., "Go from LA to NY")
- **Journey Options**: Multiple paths to achieve the goal, each with tradeoffs
  - Road trip: scenic, slow, cheaper
  - Flight: fast, expensive, efficient
  - Train: balanced
- Explorer surfaces these tradeoffs so user can choose based on their context
