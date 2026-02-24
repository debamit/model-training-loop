---
name: conversation-simulator
description: Simulates user conversations with bots. Gets bot API endpoint, reads user context, and runs multi-turn conversations to test bot behavior. Outputs transcript for analysis.
trigger: simulate conversation, test bot, replay conversation, conversation simulation, run bot test
---

# Conversation Simulator

You simulate conversations with bots to test their behavior. This skill is used when you need to act as a user and have a multi-turn conversation with a bot.

## How It Works

### Step 1: Gather Information

Ask the user for:
1. **Bot API URL** - The endpoint to send messages to
2. **Conversation Goal** - What the simulated user wants to accomplish
3. **Number of turns** - How many messages to exchange (default: 5)

If user context is needed, read from `user_context.json`:
```
Use read_file to read user_context.json
```

### Step 2: Prepare Request

Format the API request. Most bot APIs expect:
```json
{
  "message": "user message",
  "context": { ...user context... },
  "goal": "conversation goal"
}
```

### Step 3: Execute Conversation

Use shell or fetch_url to send requests to the bot API. Example using curl:
```
shell: curl -X POST <BOT_API_URL> -H "Content-Type: application/json" -d '{"message": "hello", "context": {...}}'
```

### Step 4: Save Transcript

After each turn, save the conversation to a transcript file. Use:
- `write_file` to create `sessions/simulated_conversation_{timestamp}.json`

## Testing: Mock Bot

For testing, use this simple mock bot running locally:

**Start mock server:**
```bash
cd /home/debamit007/model-training-loop
python -m http.server 8080 --directory mock_bot
```

**Mock bot endpoint:** `http://localhost:8080/chat`

The mock bot responds with:
- Echoes back your message
- Adds a simple response based on keywords
- Maintains conversation context

## Example Interaction

User: "Simulate a conversation with a travel bot"

1. Ask: "What's the bot API URL?" (or use mock: http://localhost:8080/chat)
2. Ask: "What's the conversation goal?" (e.g., "book a flight")
3. Read user_context.json for context
4. Run conversation:
   - Turn 1: "I want to book a flight"
   - Bot responds
   - Turn 2: "To Paris"
   - Bot responds
   - etc.
5. Save transcript to `sessions/simulated_conversation_{timestamp}.json`

## Output Format

Save transcript as JSON:
```json
{
  "goal": "book a flight",
  "bot_api": "http://localhost:8080/chat",
  "user_context": { ... },
  "turns": [
    {
      "turn": 1,
      "user_message": "I want to book a flight",
      "bot_response": "Where would you like to go?",
      "timestamp": "2026-02-24T12:00:00Z"
    }
  ]
}
```

## Commands

- **Simulate [goal]** - Start a new conversation simulation
- **Run test** - Use mock bot to test
- **Show transcript** - Display last saved transcript
