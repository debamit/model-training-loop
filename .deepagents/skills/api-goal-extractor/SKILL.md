---
name: api-goal-extractor
description: Analyzes API specs to extract possible user goals and intents the bot can fulfill
trigger: analyze api, extract goals, api capabilities, what can the bot do, intent discovery
---

# API Goal Extractor

Analyzes an API specification (OpenAPI/Swagger) and extracts all possible user goals/intents the bot can handle.

## Goal File Location

**Goals are stored in:** `specs/<api_name>_goals.json`

Examples:
- Petstore API: `specs/petstore_goals.json`
- Shopify API: `specs/shopify_goals.json`
- Weather API: `specs/weather_goals.json`

To find all available goal files, use: `specs/*_goals.json`

## Step 1: Get the API Spec

Ask user for:
- File path to API spec (JSON/YAML) - use relative path from working directory
- Or URL to the spec

If user says "figure it out", check common locations (use relative paths from working directory `/home/debamit007/model-training-loop`):
- `specs/`
- `*.json`
- Use `specs/*` pattern (NOT `specs/**/*` - recursive glob is broken)

## Step 2: Read and Analyze the Spec

Read the spec file. For each endpoint in the spec:
1. Note the HTTP method (GET, POST, PUT, DELETE, etc.)
2. Note the path (e.g., `/pet/findByStatus`)
3. Note the summary/description from the spec
4. Note required parameters and their types

## Step 3: Map Endpoints to User Goals

For each endpoint, think from a USER'S perspective - what would a real person want to accomplish? Not what the API does, but WHY someone would use it.

| Instead of... | Think like a user who wants to... |
|---------------|-----------------------------------|
| "GET /products" | "Find/buy products" |
| "POST /orders" | "Place an order" |
| "GET /orders/{id}" | "Track my order" |
| "DELETE /orders/{id}" | "Cancel my order" |
| "POST /pet" | "Sell/list a pet" |
| "GET /pet/findByStatus" | "Adopt a pet" |
| "PUT /pet/{id}" | "Update my pet" |
| "DELETE /pet/{id}" | "Remove delist my pet" |

The user goal should be:
- In natural language ("Adopt a pet", "Track my order")
- Something a non-technical person would say
- Focused on the outcome, not the mechanism

## Step 4: Save Goals to File

Generate filename from spec name by appending `_goals.json`:
- `specs/petstore.json` → `specs/petstore_goals.json`
- `specs/shopify.json` → `specs/shopify_goals.json`
- `specs/weather.json` → `specs/weather_goals.json`

**Location hint:** Always save to `specs/` directory in the working directory `/home/debamit007/model-training-loop`.

Save format:
```json
{
  "spec": "<spec_path>",
  "location": "specs/<api_name>_goals.json",
  "goals": [
    {
      "id": 1,
      "user_goal": "<user-friendly goal>",
      "description": "<what this goal accomplishes>",
      "api_calls": ["<HTTP_METHOD> /endpoint"]
    }
  ],
  "simulated": [],
  "last_updated": "<YYYY-MM-DD>"
}
```

Save to: `<spec_path_without_extension>_goals.json`

## Step 5: Present Goals to User

Format the extracted goals from the USER'S perspective:

```markdown
## What You Can Do With This Bot

1. **<Goal 1>** - <description>
2. **<Goal 2>** - <description>
...
```

Show all goals with their IDs. Ask: "Which goal would you like to simulate?"

## Step 6: Ask User to Select

Ask: "Which goal would you like to simulate?"

Wait for user to pick one, then return the selected goal.
