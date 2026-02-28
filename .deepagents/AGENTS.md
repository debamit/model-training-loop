# Agent Memory

## ⚠️ CRITICAL: Always Use Skills First

**IMPORTANT: Skills are NOT tools. They are documentation you must READ.**

1. **Skills are documents to READ**, not tools to call
2. Before using a skill, read its SKILL.md file first
3. Use the TOOLS (shell, read_file, etc.) to execute what the skill describes

### How Skills Work

```
User: "extract goals from pdf"

WRONG (treating skill as tool):
  → calls "pdf-finder" as if it were a function

RIGHT (read skill first, then execute):
  1. read_file(".deepagents/skills/pdf-finder/SKILL.md")
  2. Understand: skill says use glob to find PDFs
  3. Use glob tool to find the PDF
  4. read_file(".deepagents/skills/pdf-reader/SKILL.md")  
  5. Use shell to run Python/pdfplumber code
  6. Continue chain...
```

### Available Skills (READ each one before using)

| Skill | Purpose | Trigger |
|-------|---------|---------|
| pdf-finder | Find PDF files | find pdf, locate pdf |
| pdf-reader | Extract text from PDF | read pdf, extract pdf text |
| pdf-goal-mapper | Map PDF content to goals | extract goals from pdf |
| pdf-goal-saver | Save goals to JSON | save pdf goals |
| api-spec-handler | Find and read API spec files | find api spec, read api spec |
| api-goal-mapper | Map API endpoints to goals | extract goals from api |
| api-goal-saver | Save API goals to JSON | save api goals |
| bot-simulation | Simulate bot conversations | simulate chat |
| skill-author | Help create new skills | create skill |

### Skill Workflow

For "extract goals from pdf":
1. **read_file** pdf-finder/SKILL.md → use glob to find PDF
2. **read_file** pdf-reader/SKILL.md → extract text using Python
3. **read_file** pdf-goal-mapper/SKILL.md → analyze text, extract goals
4. **read_file** pdf-goal-saver/SKILL.md → save goals to JSON

---

## Project: Model Training Loop

## Available Tools

**File tools:**
- read_file: Read file contents
- write_file: Create or overwrite files
- edit_file: Modify existing files
- ls: List directory contents
- glob: Find files by pattern
- grep: Search file contents

**Other tools:**
- shell: Run shell/Python commands
- web_search: Search the web
- http_request: Make HTTP API calls
- task: Spawn subagents
- get_country_info: Get country details

## Key Files

- `cli/main.py` - Main CLI entry point
- `sessions/checkpoints.db` - SQLite database
- `.deepagents/skills/` - Available skills (READ THESE)
