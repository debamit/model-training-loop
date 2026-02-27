---
name: api-goal-mapper
description: Map API endpoints to user-friendly goals/intents
trigger: extract goals from api, api capabilities, api intents, what can i do with this api
---

# API Goal Mapper

Analyze API spec and extract user-friendly goals/intents.

## Input

- Parsed API spec (from api-spec-reader)
- API name (from filename)

## Process

For each endpoint, convert API terminology to user goals:

| Instead of... | Think like a user who wants to... |
|---------------|-----------------------------------|
| "GET /products" | "Find/buy products" |
| "POST /orders" | "Place an order" |
| "GET /orders/{id}" | "Track my order" |
| "DELETE /orders/{id}" | "Cancel my order" |
| "POST /pet" | "Sell/list a pet" |
| "GET /pet/findByStatus" | "Adopt a pet" |

## Goal Format

```json
{
  "id": 1,
  "user_goal": "Adopt a pet",
  "description": "Find pets available for adoption",
  "api_calls": ["GET /pet/findByStatus"]
}
```

## Output

Return list of goal objects. Do NOT save to file - use api-goal-saver.
