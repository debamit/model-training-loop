# Session Checkpoint

## Completed (as of Feb 21, 2026)

| Component | File | Status |
|-----------|------|--------|
| DeepAgent Integration | `cli/main.py` | ✅ |
| MiniMax API (Anthropic-compatible) | `.env`, `config.json` | ✅ |
| Configurable Model/Provider | `config.json`, `config/__init__.py` | ✅ |
| SQLite-based Persistent Storage | `langgraph.checkpoint.sqlite` | ✅ NEW |
| Session Persistence | `sessions/checkpoints.db` | ✅ NEW |
| CLI with session management | `cli/main.py` | ✅ |

---

## Migration: JSON → SQLite (Feb 21, 2026)

### What Changed
- **Removed:** Custom `JsonCheckpointSaver` implementation in `storage/`
- **Removed:** `--list-sessions` CLI flag (query DB directly instead)
- **Added:** `langgraph-checkpoint-sqlite` dependency
- **Added:** Single SQLite database file (`sessions/checkpoints.db`)

### Why
- JSON was too noisy with extra metadata files
- SQLite is cleaner, more efficient, and built-in to Python
- Can query sessions directly with SQL if needed

### Query Sessions Directly
```python
import sqlite3
conn = sqlite3.connect("sessions/checkpoints.db")
cur = conn.cursor()
cur.execute("SELECT thread_id, checkpoint_id FROM checkpoints")
```

---

## Current File Structure

```
.env                      # API keys (MiniMax, Anthropic, etc.)
config.json               # Provider/model config (MiniMax default)
config/__init__.py        # Config loader module
sessions/
  checkpoints.db          # SQLite database (checkpoints + writes)
cli/main.py               # CLI with session management
agent/
  logging_middleware.py   # Tools: log_goal, log_step, complete_journey
  country_tool.py         # Tool: get_country_info
tools/
  llm_client.py
  builder_tool.py
  mock_tool.py
schemas/
  goal.py
  journey.py
```

---

## How to Run

```bash
# New session (one-shot)
python -m cli.main "Hello, my name is Bob"

# Resume session
python -m cli.main --session-id <SESSION_ID> "What is my name?"

# Config override
python -m cli.main --provider minimax --model MiniMax-M2.1 "Hello"

# Interactive mode
python -m cli.main

# Disable auto-export to conversation.json
python -m cli.main --no-export "Hello"
```

---

## Dependencies

```
pydantic>=2.0
anthropic>=0.18.0
python-dotenv>=1.0.0
deepagents>=0.0.1
langgraph>=1.0.0
langgraph-checkpoint-sqlite>=1.0.0
requests
```

---

## Next Steps (Priority Order)

1. **Explorer Agent** - Analyze conversation history, create/update goals, generate reports
2. **Agent Filesystem** - Use FilesystemBackend for agent file access
3. **Session metadata** - Add created_at, last_message tracking
4. **Interactive mode improvements** - Better UX

---

## Vector Search Options (Researched, Deferred)

- **PostgreSQL** - Required for LangGraph Store with vector search (needs Docker)
- **Chroma** - Local vector DB option (separate from SQLite)
- **Deferred** - Keeping SQLite simple for now

---

## Key Philosophy (from WORKFLOW.md)

- Iteration over one-shotting
- K.I.S.S. (Keep It Stupidly Simple)
- Defer features for iteration speed
- Smallest incremental value for enhancements
