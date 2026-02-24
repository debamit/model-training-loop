# Session Checkpoint

## Completed (as of Feb 24, 2026)

| Component | File | Status |
|-----------|------|--------|
| DeepAgent Integration | `cli/main.py` | ✅ |
| MiniMax API (Anthropic-compatible) | `.env`, `config.json` | ✅ |
| Configurable Model/Provider | `config.json`, `config/__init__.py` | ✅ |
| SQLite-based Persistent Storage | `langgraph.checkpoint.sqlite` | ✅ |
| Session Persistence | `sessions/checkpoints.db` | ✅ |
| CLI with session management | `cli/main.py` | ✅ |
| Conversation Analyzer Skill | `.deepagents/skills/conversation-analyzer/SKILL.md` | ✅ NEW |
| DeepAgents CLI Integration | `~/.deepagents/config.toml` | ✅ NEW |
| Multi-session Analysis | `cli/analyze.py` | ✅ NEW |

---

## New Architecture: DeepAgents Skills (Feb 24, 2026)

### What Changed
- **Added:** `.deepagents/` directory with skills and AGENTS.md
- **Added:** `deepagents-cli` for official LangChain DeepAgents CLI
- **Added:** Skills-based architecture for extensibility
- **Removed:** Deprecated logging tools (`log_goal`, `log_step`)

### Two CLI Setup

| CLI | Command | API | Use Case |
|-----|---------|-----|----------|
| **Your CLI** | `python -m cli.main` | MiniMax (direct) | Custom tools, specific workflows |
| **Official CLI** | `deepagents` | MiniMax (via Anthropic compat) | Skills, memory, project context |

### Configuration

**MiniMax via deepagents CLI** (`~/.deepagents/config.toml`):
```toml
[models.providers.anthropic]
base_url = "https://api.minimax.io/anthropic"
api_key_env = "MINIMAX_API_KEY"
models = ["MiniMax-M2.1", "MiniMax-M2.5"]

[models]
default = "anthropic:MiniMax-M2.5"

[shell]
timeout = 300
```

**API Key** (set in environment):
```bash
export MINIMAX_API_KEY="sk-cp-pXxGHLe-..."
```

---

## Skills Architecture

### Directory Structure
```
.deepagents/
├── AGENTS.md                    # Agent memory/instructions
└── skills/
    └── conversation-analyzer/
        └── SKILL.md             # Intent classification skill
```

---

## Project Philosophy

### Skills Architecture

Skills are self-contained in `.deepagents/skills/<skill-name>/SKILL.md`.
- **No Python code** unless enforcing explicit user constraints
- Use built-in tools: `read_file`, `write_file`, `shell`, conversation
- See `skill-author` skill for how to create new skills

### Available Skills

| Skill | Purpose | Trigger |
|-------|---------|---------|
| `conversation-analyzer` | Classify intent (Query/Action/Preference), measure quality | "analyze conversation", "classify intent" |
| `user-context-simulator` | Manage 4-layer user context (Physical, Mental, User Context, Explicit Preferences) | "manage user context", "simulate user", "preferences" |
| `conversation-simulator` | Simulate multi-turn conversations with bots via API | "simulate conversation", "test bot", "replay conversation" |
| `skill-author` | How to create new skills | "create skill", "write skill" |

### How Skills Work
1. Agent detects task matches skill trigger
2. Reads SKILL.md for instructions
3. Executes using provided tools/commands
4. Outputs structured analysis

---

## Current File Structure

```
.env                      # API keys (MiniMax)
config.json               # Provider/model config
config/__init__.py        # Config loader
user_context.json         # User preferences/context (4 layers)
sessions/
  checkpoints.db          # SQLite database
mock_bot/
  bot.py                  # Mock bot for testing
  index.html              # Mock bot info page
cli/
  main.py                 # CLI entry point
  analyze.py              # Multi-session analysis
agent/
  __init__.py
  conversation_analyzer.py  # Analysis logic
  country_tool.py         # Tool: get_country_info
.deepagents/
  AGENTS.md               # Agent memory
  skills/
    skill-author/
      SKILL.md            # How to create skills
    conversation-analyzer/
      SKILL.md            # Intent classification
    user-context-simulator/
      SKILL.md            # User context management
    conversation-simulator/
      SKILL.md            # Bot conversation simulation
analysis/
  chat_Analysis_*.json   # Goal-based analysis
  intent_analysis_*.json # Intent classification
schemas/
  analysis.py
```

---

## How to Run

### Your CLI (MiniMax direct)
```bash
# New session (one-shot)
python -m cli.main "Hello"

# Interactive mode
python -m cli.main

# Analyze sessions
python -m cli.analyze b7a8bfbd
python -m cli.analyze b7a8bfbd 7abf43e0  # Multiple sessions
python -m cli.analyze --list
```

### Official DeepAgents CLI (with skills)
```bash
# Set API key
export MINIMAX_API_KEY="sk-cp-pXxGHLe-..."

# Interactive mode
deepagents --model anthropic:MiniMax-M2.5

# Non-interactive with skill
deepagents --model anthropic:MiniMax-M2.5 -n "Analyze session b7a8bfbd for intent"

# List skills
deepagents skills list
```

---

## Intent Classification Output

```json
{
  "conversation_id": "b7a8bfbd",
  "total_turns": 12,
  "total_human_turns": 2,
  "intents": {
    "query": 1,
    "action": 1,
    "preference": 0
  },
  "quality": {
    "avg_sentiment": "positive",
    "clarity_issues": 0,
    "follow_ups": 1
  },
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

---

## Dependencies

```
pydantic>=2.0
anthropic>=0.18.0
python-dotenv>=1.0.0
deepagents>=0.0.1
deepagents-cli>=0.0.25
langgraph>=1.0.0
langgraph-checkpoint-sqlite>=1.0.0
requests
```

---

## Next Steps (Priority Order)

1. **Evidence Builder** - Gather evidence for answers (github repos, links, PDFs, swaggers)

2. ~~`conversation-simulator`~~ - ✅ Done (tested with mock bot)

3. ~~`user-context-simulator`~~ - ✅ Done (4-layer: Physical, Mental, User Context, Explicit Preferences)

4. ~~`skill-author`~~ - ✅ Done (meta-skill for creating skills)

5. **Skill Creator** - Use built-in skill to create new skills

---

## Key Philosophy (from WORKFLOW.md)

- Iteration over one-shotting
- K.I.S.S. (Keep It Stupidly Simple)
- Defer features for iteration speed
- Smallest incremental value for enhancements
