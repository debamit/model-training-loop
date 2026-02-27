# Model Training Loop - Deep Agent

A personal AI assistant CLI built on LangChain DeepAgents with SQLite checkpointing, designed to work efficiently with smaller models (14B and under).

## What This Agent Is

A self-training AI assistant that:
- Uses skills to break down tasks into focused, single-action steps
- Checkpoints conversations to SQLite for analysis and improvement
- Designed to work with smaller, more efficient models rather than large foundation models

## Target Users

- Developers who want a local, personal AI assistant
- Users running smaller models (8B-14B) who need structured workflows
- Anyone wanting to analyze documents (PDFs, APIs) to extract user intents/goals

## Architecture

### Core Philosophy
Two-pass workflow: **Builder** (fast answers) → **Auditor** (skeptical verification)

### 6-Skill System (Future)
| Skill | Purpose |
|-------|---------|
| A | Goal & Journey Generator - extract intent, log interactions |
| B | Builder (Day) - fast answers, tight budgets |
| C | Builder (Night) - offline exploration, find better answers |
| D | Auditor - skeptical review, prompt-injection defense |
| E | Orchestrator - routes requests, enforces budgets |
| F | Nightly Replay - self-training, propose preference updates |

### Key Concepts
- **Weights**: User intents/goals (what user wants)
- **Biases**: Tool calls, sources, LLM workflow (how we get there)
- **Weighs-n-Biases.md**: Local storage of learned patterns
- **Canary Harness**: Trick questions to detect alignment drift

## Available Skills

### Document Analysis Skills
| Skill | Purpose |
|-------|---------|
| pdf-finder | Locate PDF files in common locations |
| pdf-reader | Extract text from PDF using pdfplumber |
| pdf-goal-mapper | Analyze PDF content, extract user intents |
| pdf-goal-saver | Save extracted goals to JSON |

### API Analysis Skills
| Skill | Purpose |
|-------|---------|
| api-spec-finder | Locate API specification files (OpenAPI/Swagger) |
| api-spec-reader | Parse JSON/YAML API specs |
| api-goal-mapper | Map API endpoints to user-friendly goals |
| api-goal-saver | Save extracted goals to JSON |

### Utility Skills
| Skill | Purpose |
|-------|---------|
| bot-simulation | Simulate conversations with bots |
| skill-author | Guide for creating new skills |

## Design Principles for Smaller Models

### One Action Per Skill
Each skill does exactly ONE thing. This prevents confusion when using smaller models with limited context understanding.

### Explicit Triggers
Triggers are specific and mutually exclusive to avoid wrong skill selection.

### Minimal Context
Keep SKILL.md under 100 lines. Smaller models parse less reliably with longer context.

### Composability
Model calls skills in sequence rather than using "master" skills that do everything.

### Workflow Example

User says: "extract goals from pdf"

```
1. read_file pdf-finder/SKILL.md → use glob to find PDF
2. read_file pdf-reader/SKILL.md → extract text with Python
3. read_file pdf-goal-mapper/SKILL.md → analyze, extract goals
4. read_file pdf-goal-saver/SKILL.md → save to JSON
```

See [ARCHITECTURE.md](./ARCHITECTURE.md) for visual diagrams.

## Current State

- Skills refactored for smaller model compatibility (14B and under)
- Project-level AGENTS.md configured with skill instructions
- PDF and API goal extraction working
- Session checkpointing to SQLite

## Key Files

| File | Purpose |
|------|---------|
| `cli/main.py` | Main CLI entry point |
| `sessions/checkpoints.db` | SQLite database for conversation history |
| `.deepagents/AGENTS.md` | Agent memory and instructions |
| `.deepagents/skills/` | Available skills (each is a directory with SKILL.md) |
| `ARCHITECTURE.md` | Architecture diagrams |

## Tech Stack

- Python 3.12
- LangChain + DeepAgents
- SQLite (checkpoints)
- pdfplumber (PDF extraction)
- PyYAML (API spec parsing)

## Getting Started

1. Place files to analyze in:
   - PDFs: `knowledge-base/pdf/`
   - API specs: `specs/`

2. Common commands:
   - "find pdf" → locate PDF files
   - "read pdf" → extract text
   - "extract goals from pdf" → full analysis pipeline
   - "find api spec" → locate API specs
   - "extract goals from api" → analyze API and extract goals
