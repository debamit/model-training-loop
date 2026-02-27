---
name: api-goal-saver
description: Save extracted API goals to a JSON file
trigger: save api goals, write goals to file, persist api intents
---

# API Goal Saver

Save extracted API goals to a JSON file.

## Input

- API spec path (original spec file)
- Goals list (from api-goal-mapper)
- API name

## Output Location

Save to: `specs/<api_name>_goals.json`

Example: `specs/petstore.json` → `specs/petstore_goals.json`

## JSON Format

```json
{
  "spec": "<spec_path>",
  "location": "specs/<api_name>_goals.json",
  "goals": [
    {
      "id": 1,
      "user_goal": "<natural language goal>",
      "description": "<what this accomplishes>",
      "api_calls": ["<METHOD> /endpoint"]
    }
  ],
  "simulated": [],
  "last_updated": "<YYYY-MM-DD>"
}
```

## Steps

1. Extract API name from spec filename
2. Construct output path: `specs/{name}_goals.json`
3. write_file JSON
4. Confirm save location
