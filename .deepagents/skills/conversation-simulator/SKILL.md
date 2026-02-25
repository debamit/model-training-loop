---
name: conversation-simulator
description: Simulates user conversations with bots. Supports both real API calls and LLM-based simulation from API specs (swagger/curl/manual). Reads user context, runs multi-turn conversations, outputs transcript for analysis.
trigger: simulate conversation, test bot, replay conversation, conversation simulation, run bot test, simulate from swagger, simulate from api spec, test bot capabilities
---

# Conversation Simulator

You simulate conversations with bots to test their behavior. This skill supports two modes:

1. **Live Mode**: Calls real bot API endpoints
2. **Simulation Mode**: Uses LLM to simulate bot responses from API specs (no real API calls)

## Mode 1: Live Mode (Real API Calls)

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

---

## Mode 2: Simulation Mode (LLM-Based - No Real API Calls)

Use this mode for fast prototyping. The LLM simulates bot responses based on API specs.

### When to Use Simulation Mode

- "Simulate from swagger", "test bot from API spec"
- "Test what questions this bot can answer"
- "Prototype conversation without calling real API"
- When user provides: swagger file, curl commands, or API description

### Step 1: Gather API Spec

Ask the user for one of:
1. **Path to swagger/OpenAPI file** (JSON or YAML)
2. **URL to swagger/OpenAPI endpoint**
3. **Curl commands** (extract endpoints from curl)
4. **Manual description** of bot capabilities

Read the spec using `read_file` or fetch with `webfetch`.

### Step 2: Parse API Spec

Extract available endpoints and tools. Create a summary like:

```
## Bot Capabilities

### Endpoints:
- GET /weather?city={city} - Get weather for a city
- POST /book - Book a flight
- GET /hotels?location={location}&checkin={date}&checkout={date} - Search hotels

### Tools:
- get_weather(city: string) - Returns weather info
- book_flight(from: string, to: string, date: string) - Books flight
- search_hotels(location: string, checkin: string, checkout: string) - Lists hotels
```

### Step 3: Get User Context

Read `user_context.json` for simulated user profile:
```
read_file: user_context.json
```

### Step 4: Simulate Conversation (Use LLM)

For each turn, invoke the LLM with this prompt structure:

```
You are simulating a bot with these capabilities:
{parsed API spec from Step 2}

User context:
{user context from Step 3}

Conversation history:
{previous turns}

Now respond as the bot would to:
User: {current user message}

Respond in character as the bot. If you need to call a tool, describe what tool would be called and what it would return. If you can't fulfill the request based on your capabilities, say so.
```

### Step 5: Save Transcript

Save to `sessions/simulated_conversation_{timestamp}.json`

---

## Testing: Mock Bot

For testing live mode, use this simple mock bot running locally:

**Start mock server:**
```bash
cd /home/debamit007/model-training-loop
python mock_bot/bot.py
```

**Mock bot endpoint:** `http://localhost:8080/chat`

The mock bot responds with keyword-based responses.

---

## Example Interactions

### Live Mode Example:
User: "Simulate a conversation with a travel bot"

1. Ask: "Live API or simulation mode?"
2. If live: Ask for bot API URL
3. Ask: "What's the conversation goal?" (e.g., "book a flight")
4. Read user_context.json for context
5. Run conversation via API calls
6. Save transcript

### Simulation Mode Example:
User: "Test what questions can be answered by the weather bot using its swagger"

1. Ask: "Provide the swagger file or URL"
2. User provides: `~/apis/weather-bot-swagger.json`
3. Read and parse the swagger
4. Ask: "What's the conversation goal?" (e.g., "check weather and book trip")
5. Read user_context.json
6. Run LLM-based simulation:
   - Turn 1: User: "What's the weather?"
   - LLM responds as bot: "Which city would you like to check?"
   - Turn 2: User: "Paris"
   - LLM responds: "Paris is sunny, 22°C. Would you like me to book a trip?"
7. Save transcript

---

## Output Format

Save transcript as JSON:
```json
{
  "goal": "book a flight",
  "mode": "simulation",
  "api_spec_source": "swagger.json",
  "simulation_model": "MiniMax-M2.5",
  "user_context": { ... },
  "turns": [
    {
      "turn": 1,
      "user_message": "I want to book a flight",
      "bot_response": "Where would you like to fly from and to?",
      "simulated_tools": [],
      "timestamp": "2026-02-24T12:00:00Z"
    },
    {
      "turn": 2,
      "user_message": "From NYC to Paris",
      "bot_response": "Great! What dates are you looking at?",
      "simulated_tools": [],
      "timestamp": "2026-02-24T12:00:01Z"
    }
  ]
}
```

For live mode, `mode` is "live" and `api_spec_source` is the bot URL instead.

---

## Commands

- **Simulate [goal]** - Start new simulation (asks for mode)
- **Simulate from [swagger file]** - Start simulation mode directly
- **Test bot [url]** - Start live mode with real API
- **Run test** - Use mock bot to test
- **Show transcript** - Display last saved transcript
- **List capabilities** - Parse and show available endpoints from spec
