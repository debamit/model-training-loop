# Workflow Philosophy

## Core Principles

### 1. Iteration Over One-Shotting
- Smaller, quicker iterations over longer iteration cycles
- Course correct sooner rather than later
- Keep the project flexible and nimble

### 2. K.I.S.S. (Keep It Stupidly Simple)
- For new features: minimum required to achieve the feature
- For enhancements: smallest possible incremental value
- Push back if scope becomes too ambitious

### 3. Iteration Speed Over Features
- Defer complex features (nightly replay, self-training) until core is solid
- Build incrementally, validate often

## Current MVP Scope

**Skill A: Goal & Journey Logger**
- Define canonical schema for goals and journeys
- Implement basic logging infrastructure
- No other skills until Skill A is complete and validated

## Future Phases

| Phase | Skills | Description |
|-------|--------|-------------|
| 1 (Current) | A | Schema & logger |
| 2 | B | Builder (day) - fast answers |
| 3 | D | Auditor - skeptical review |
| 4 | C, F | Nightly exploration & replay |

## Reference

- LangGraph DeepAgents: https://github.com/langchain-ai/deepagents
