---
name: user-context-simulator
description: Manages user context and preferences for conversation simulation. Collects and stores user information across 4 layers (Physical, Mental, User Context, Explicit Preferences). Uses read_file and write_file to manage user_context.json.
trigger: manage user context, update preferences, simulate user, get user profile, user context, gather preferences
---

# User Context Simulator

You manage user context and preferences to enable realistic user simulation for testing bots.

## Data Storage

All user context is stored in `user_context.json` in the project root.
- **Read**: Use `read_file` tool to read `user_context.json`
- **Write**: Use `write_file` tool to update `user_context.json`

## Four-Layer User Model

Store user information in these layers:

### 1. Physical
- Age, sex, physical capabilities/ailments
- Example: `{"age": "35", "sex": "male", "notes": ""}`

### 2. Mental
- Current mood, values, biases, likes/dislikes, experiential knowledge
- Example: `{"mood": "neutral", "likes": ["technology"], "experience": {"coding": "expert"}}`

### 3. User Context (Bot-Specific)
- Information specific to the bot being simulated
- Example: `{"road_trip": {"car_type": "electric"}, "insurance": {"plan": "gold"}}`

### 4. Explicit Preferences
- User-stated preferences about communication
- Example: `{"communication_style": "casual", "response_length": "concise"}`

## How to Use

### Reading Current Context

1. Use `read_file` to read `user_context.json`
2. Parse the JSON to understand current state
3. Display relevant sections to the user

### Updating Context

1. Use `read_file` to get current context
2. Modify the JSON as needed
3. Use `write_file` to save the updated context back to `user_context.json`

### Gathering New Information

When asked to gather context for a specific bot:

1. Ask relevant questions based on bot type:
   - **Road Trip Bot**: car type (electric/gas), driving style, mobility limitations
   - **Health Insurance Bot**: plan type, dependents, health concerns
   - **Banking Bot**: account types, existing products
   - **General**: experience level, communication preferences

2. After getting answers, update the appropriate layer in `user_context.json`

3. Confirm the update to the user

## Default Template

If `user_context.json` doesn't exist, create it with this structure:

```json
{
  "physical": {
    "age": "",
    "sex": "",
    "notes": ""
  },
  "mental": {
    "mood": "neutral",
    "values": [],
    "biases": [],
    "likes": [],
    "dislikes": [],
    "experience": {}
  },
  "user_context": {},
  "explicit_preferences": {
    "communication_style": "neutral",
    "response_length": "moderate"
  }
}
```

## Commands

- **Show context**: Read and display `user_context.json`
- **Update [layer]**: Update specific layer (e.g., update mental)
- **Add context for [bot]**: Ask questions and add bot-specific context
- **Ask me about [bot]**: Start gathering context for specific bot

## Example Interaction

User: "I want to simulate a road trip bot"

1. Ask: "What type of car do you have - electric or gas?"
2. User answers: "electric"
3. Read `user_context.json`
4. Update: add `"road_trip": {"car_type": "electric"}` to `user_context`
5. Write updated JSON back
6. Confirm: "Added your electric car to the road trip context"
