---
name: bot-simulation
description: Simulates bot conversations using LLM. No real API calls.
trigger: simulate bot, simulate from swagger, simulate from api spec, mock bot test, test bot capabilities
---

# Bot Simulation

Simulate a conversation between a user and a bot. You are the agent running the simulation.

## Step 1: Get the Goal and Spec

Ask user for:
1. Goal ID (from goals file) - OR -
2. New goal description (if not using goals file)

Also ask for the bot API spec:
- File path (e.g., `specs/petstore.json`)
- URL
- Or use one already in `specs/`

## Step 1b: Check for Existing Goals File

If user provides a spec path (e.g., `specs/petstore.json`):
1. Check if `specs/petstore_goals.json` exists
2. If exists, show available goals (filter out already simulated ones)
3. Ask user to pick from available goals OR enter new goal

Example prompt:
```
Available goals (not yet simulated):
1. Adopt a pet
2. Sell a pet
...
Already simulated: Track order

Which goal? (enter number or describe new goal)
```

## Step 2: Confirm Goal with User

Repeat the goal back to the user. Ask: "Is this correct? Should I start?"

Wait for user to say yes.

## Step 3: Get the Bot Capabilities

If user gave a file path or URL, read it.
If user gave a description, use that.

Write down what the bot can do.

## Step 4: Run the Conversation

For each turn:
1. You generate a user message
2. You generate a bot response
3. You document the bot's reasoning and evidence

User message: Something a real person would say to achieve the goal.
Bot response: Based on what the bot can do from Step 3.

For each turn, also capture:
- **bot_reasoning**: Why the bot responded this way (what it inferred, what it needs)
- **apis_called**: List of API endpoints called in this turn (e.g., ["GET /store/order/{orderId}"])
- **evidence**: Key fields/values from API responses that informed the response

Stop when the goal is achieved. Do not use a fixed number of turns.

## Step 5: Save the Conversation

Generate timestamp using: date +%Y%m%d_%H%M%S

Save to: /home/debamit007/model-training-loop/sessions/simulated_conversation_{timestamp}.json

Format:
```json
{
  "goal": "user goal here",
  "goal_id": 7,
  "mode": "simulation",
  "api_spec_source": "URL or file path",
  "turns": [
    {
      "turn": 1,
      "user_message": "what the user says",
      "bot_response": "what the bot says",
      "bot_reasoning": "why the bot responded this way",
      "apis_called": ["GET /store/order/{orderId}"],
      "evidence": {
        "orderId": "User provided: 5",
        "status": "From API response: placed",
        "petId": "From API response: 1"
      }
    }
  ]
}
```

## Step 6: Update Goals File

If a goals file exists for this spec:
1. read_file the goals file
2. Add the goal_id to the "simulated" array
3. write_file back to the goals file

Example update:
```json
{
  "spec": "specs/petstore.json",
  ...
  "simulated": [2, 7],  // added goal ID 7
  ...
}
```

## Rules
- Do not make real API calls
- Bot can only do what is in the spec
- If user asks for something the bot cannot do, the bot should say it cannot do that
- Always confirm goal with user before starting
- Stop when goal is achieved
