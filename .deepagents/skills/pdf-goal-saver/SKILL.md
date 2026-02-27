---
name: pdf-goal-saver
description: Save extracted PDF goals to a JSON file
trigger: save pdf goals, write goals to file, persist pdf intents
---

# PDF Goal Saver

Save extracted PDF goals to a JSON file.

## Input

- PDF path (original PDF file)
- Goals list (from pdf-goal-mapper skill)
- Document type (e.g., "Invoice", "Health Insurance Plan")

## Output Location

Save to: `knowledge-base/pdf/<pdf_name>_goals.json`

Examples:
- `invoice.pdf` → `knowledge-base/pdf/invoice_goals.json`
- `m-24-pb-in-944339-planbrochure.pdf` → `knowledge-base/pdf/m-24-pb-in-944339-planbrochure_goals.json`

## JSON Format

```json
{
  "source": "<pdf_path>",
  "location": "knowledge-base/pdf/<pdf_name>_goals.json",
  "document_type": "<type>",
  "goals": [
    {
      "id": 1,
      "user_goal": "<natural language goal>",
      "description": "<what this accomplishes>",
      "capabilities": ["<action1>", "<action2>"]
    }
  ],
  "simulated": [],
  "last_updated": "<YYYY-MM-DD>"
}
```

## Steps

1. Extract PDF filename (without path and extension)
2. Construct output path: `knowledge-base/pdf/{filename}_goals.json`
3. write_file JSON with format above
4. Confirm save location to user
