# Explorer Agent - Scope Clarification

## Current Understanding

**What we have:**
- DeepAgent: handles user conversations, stores messages in LangGraph
- Schemas: Goal and Journey Pydantic models exist
- Goals: Create an "Explorer" agent that analyzes conversation history

**Proposed behavior:**
1. Runs on-demand (user triggers it)
2. Analyzes `List[BaseMessage]` conversation history
3. Creates/updates goals.json and journeys.json files
4. Does research using tools + generates markdown report with recommendations

---

## Questions to Resolve

### 1. Input - Where does Explorer get conversation history?

- [ ] From exported JSON file (user provides path)
- [ ] From checkpointer by session ID
- [ ] Passed directly as CLI argument

Human: I think we need to make the conversation to be output to a file for now .
Lets do conversation.json to keep it simple.
The Explorer Agent can then read this file to analyze past conversations.


### 2. Output - goals.json format?
- [ ] Single file with array of goals
- [ x ] One file per goal (e.g., `goals/goal_001.json`)
- [ ] Append new entries
- [ ] Replace entire file
One file per goal . Append or update journeys when needed.
The Agent needs to have a way to parse all goals and journeys to make sure it knows when to create a new goal and when to update

### 3. Output - journeys.json format?
- [ ] Single file with array of journeys
- [ ] One file per journey
- [ ] Link to goal_id
No sepeare journeys file . All journeys tied to a goal are part of the goal.json. Don't create new journey files. 

### 4. Markdown report - What content?
- [x ] Summary of identified goals
- [x ] Recommendations for goal/journey updates
- [x ] Research findings
- [x ] List of tools/articles accessed

### 5. Explorer tools - What should it have?
- [x ] Read/write files
- [x ] Web search
- [ ] Country info tool
- [x ] Custom research tools
For now don't worry much about the tools to be used . 

### 6. CLI interface - How to invoke?
- [ ] `python -m cli.main --explorer --session-id <id>`
- [x ] `python -m cli.explorer <session_id>`
- [ ] Separate entry point

### 7. Persistence - goals/journeys across sessions?
- [ ] Long-term user memory (accumulates across sessions)
- [ ] Per-session only
- [ ] Start fresh, create new each time
Just use the file system . As stated earlier new goal.json for every new goal identified.THe journeys go in the goal file 

### 8. Mapping logic - How to match to existing goals?
- [ ] Exact string match on user_intent
- [x ] Fuzzy/semantic matching
- [ ] User confirms new vs existing
Use the LLM to parse relevant goals and see if its better to update an existing goal or create a new one.
Agent has full agency on when to create a new agent or update existing goal.

---

## Proposed File Structure

```
/explorer/
  ├── __init__.py
  ├── agent.py          # Explorer agent definition
  ├── analyzer.py       # Conversation analysis logic
  ├── goals.json        # Stored goals
  ├── journeys.json     # Stored journeys
  └── reports/          # Markdown reports
      └── 2026-02-19_report.md
```

---

## Notes

- Current logging tools are lightweight stubs (in-memory only)
- Explorer should likely have persistent file storage for goals/journeys
- Need to decide if Explorer reuses DeepAgent's tools or has its own

GOAL and Journey philosophy

Eg GOAL: Go from LA to NY

Journey options: 
a) Road trip:
  depends on whether person is willing to drive an has time
   Sub journeys:
    which route to take based on their preference
b) train:
   Amtrak with different route option at different budgets (time and money)
c) Plane

I hope you get the idea. 
for each goal there are multiple paths to get to the goal and different path carry different tradeoffs. the idea is to understand the different tradeoffs and make it transparent to the user . Also user may want to choose different tradeoff based on their context at that particular moment.