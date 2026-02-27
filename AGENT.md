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
