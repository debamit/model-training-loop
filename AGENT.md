# Personal AI Agent with Self-Training Capabilities

## Core Philosophy
Two-pass workflow: **Builder** (fast answers) → **Auditor** (skeptical verification)

## Architecture (6 Skills)
| Skill | Purpose |
|-------|---------|
| A | Goal & Journey Generator - extract intent, log interactions |
| B | Builder (Day) - fast answers, tight budgets |
| C | Builder (Night) - offline exploration, find better answers |
| D | Auditor - skeptical review, prompt-injection defense |
| E | Orchestrator - routes requests, enforces budgets |
| F | Nightly Replay - self-training, propose preference updates |

## Key Concepts
- **Weights**: User intents/goals (what user wants)
- **Biases**: Tool calls, sources, LLM workflow (how we get there)
- **Weighs-n-Biases.md**: Local storage of learned patterns
- **Canary Harness**: Trick questions to detect alignment drift

## Workflow
1. User request → Orchestrator routes to Builder
2. Builder responds fast (day) or explores alternatives (night)
3. Auditor reviews, flags issues, challenges claims
4. User approves/rejects → weights updated
5. Nightly: replay interactions, propose better answers

## Tech Stack
- Python + LangGraph (state machines)
- LangChain + DeepAgents
- Local file storage (future: on-chain attestations)

## Current State
- Planning complete, implementation pending

## Known Issues
- glob tool with `**` (recursive) pattern doesn't work - use single-level `*` instead (e.g., `specs/*` not `specs/**/*`)

## Skill Authoring for Smaller Models (14B and under)

### Key Principles
- **One action per skill** - Each skill does exactly ONE thing. No multi-step workflows embedded in a single skill.
- **Explicit triggers** - Triggers should be specific and mutually exclusive. Avoid overlap.
- **Minimal context** - Keep SKILL.md under 100 lines. Smaller models parse less reliably with longer context.
- **Composability over convenience** - Model calls skills in sequence rather than a "master" skill that does everything.
- **No conditional logic** - Skills describe one path. Let the model handle branching by choosing different skills.

### Skill Structure Template
```markdown
---
name: <action-name>
description: <one-line what this does>
trigger: <specific phrases that match this skill>
---

# <Action Name>

## Input
- What the skill needs to work

## Code
<minimal code block>

## Output
- What this skill returns
```

### Anti-Patterns to Avoid
- ❌ "Analyze and extract" (two actions)
- ❌ Trigger: "help with pdf" (too vague)
- ❌ IF/ELSE logic inside skill
- ❌ Multi-step instructions in one skill

### Example: Refactored PDF Skills
```
pdf-finder/       → find PDF files (1 action)
pdf-reader/       → extract text (1 action)
pdf-goal-mapper/  → analyze → goals (1 action)
pdf-goal-saver/   → save to JSON (1 action)
```

When user says "analyze pdf", model calls: finder → reader → mapper → saver in sequence.

## Skill Authoring Conventions
- **Always use relative paths** in skills, never absolute paths (e.g., `specs/` not `/home/user/project/specs/`)
- Location hints should say: "relative to the current working directory where the skill is run"
- This makes skills portable across different computers
