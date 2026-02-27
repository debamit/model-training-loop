---
name: bot-live-chat
description: Simulates user conversations with bots via real API calls.
trigger: live chat, test bot api, call bot api, real bot test, chat with bot api, bot endpoint test
---

# Bot Live Chat

Simulate a conversation between a user and a bot by making real API calls.

## Step 1: Ask User for These Things

1. What is the bot API URL? (example: http://localhost:8080/chat)
2. What is the goal? (example: "book a flight", "check weather")
3. How many turns? (default: 5)

## Step 2: Run the Conversation

For each turn:
1. Send a message to the API
2. Get the bot response
3. Use the response to decide the next message

Example curl command:
```
curl -X POST <BOT_API_URL> -H "Content-Type: application/json" -d '{"message": "hello"}'
```

## Step 3: Save the Conversation

Save to: /home/debamit007/model-training-loop/sessions/live_chat_{timestamp}.json

Format:
```json
{
  "goal": "user goal here",
  "mode": "live",
  "api_url": "http://example.com/chat",
  "turns": [
    {
      "turn": 1,
      "user_message": "what the user says",
      "bot_response": "what the bot says"
    }
  ]
}
```

## Default
- 5 turns
- Output path: /home/debamit007/model-training-loop/sessions/

## Testing: Mock Bot

Start mock bot:
```
cd /home/debamit007/model-training-loop
python mock_bot/bot.py
```
Endpoint: http://localhost:8080/chat
