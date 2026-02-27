# Agent Memory

## ⚠️ CRITICAL: Always Use Skills First

**Before responding to ANY user request:**

1. **Check if a skill matches** the user's intent - read `.deepagents/skills/*/SKILL.md`
2. **If skill matches**, use ONLY that skill to complete the task
3. **If no skill matches**, then answer directly using your knowledge

### Available Skills

| Skill | Purpose | Trigger |
|-------|---------|---------|
| pdf-finder | Find PDF files | find pdf, locate pdf |
| pdf-reader | Extract text from PDF | read pdf, extract pdf text |
| pdf-goal-mapper | Map PDF content to goals | extract goals from pdf |
| pdf-goal-saver | Save goals to JSON | save pdf goals |
| api-spec-finder | Find API spec files | find api spec |
| api-spec-reader | Read API spec files | read api spec |
| api-goal-mapper | Map API endpoints to goals | extract goals from api |
| api-goal-saver | Save API goals to JSON | save api goals |
| bot-simulation | Simulate bot conversations | simulate chat |
| skill-author | Help create new skills | create skill |

### Skill Workflow

For multi-step tasks (e.g., "extract goals from pdf"):
1. Call **pdf-finder** → locate the file
2. Call **pdf-reader** → extract content  
3. Call **pdf-goal-mapper** → extract goals
4. Call **pdf-goal-saver** → save to file
5. Present result to user

---

## Project: Model Training Loop

## Available Tools

**File tools:**
- read_file: Read file contents (absolute paths)
- write_file: Create or overwrite files
- edit_file: Modify existing files
- ls: List directory contents
- glob: Find files by pattern
- grep: Search file contents

**Other tools:**
- shell: Run shell/Python commands
- web_search: Search the web
- http_request: Make HTTP API calls
- task: Spawn subagents for complex tasks
- get_country_info: Get country details (custom tool)

## Key Files

- `cli/main.py` - Main CLI entry point
- `sessions/checkpoints.db` - SQLite database storing conversation checkpoints
- `.deepagents/skills/` - Available skills
