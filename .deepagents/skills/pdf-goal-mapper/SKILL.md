---
name: pdf-goal-mapper
description: Analyze PDF content and extract user intents/goals
trigger: extract goals from pdf, pdf capabilities, pdf intents, what can i do with this pdf
---

# PDF Goal Mapper

Analyze PDF content and extract possible user goals/intents.

## Input

- PDF text content (from pdf-reader skill)
- PDF filename (for context)

## Process

Read the PDF content and think from a USER'S perspective - what would someone want to accomplish with this document?

## Document Type Guidelines

| Document Type | Example Goals |
|---------------|---------------|
| Invoice | "Pay my bill", "View charges", "Download receipt", "Dispute a charge" |
| Contract | "Sign the contract", "Review terms", "Check obligations" |
| Manual | "Learn how to use X", "Find troubleshooting", "Get setup instructions" |
| Report | "Summarize findings", "Extract key metrics", "Compare to previous" |
| Form | "Fill out the form", "Submit application", "Check requirements" |
| Insurance | "Enroll in plan", "Compare coverage", "Check benefits", "File claim" |

## Goal Format

Each goal must have:
- `id`: sequential number
- `user_goal`: natural language (what a non-technical person would say)
- `description`: what this goal accomplishes
- `capabilities`: list of related features/actions

Example:
```json
{
  "id": 1,
  "user_goal": "Pay my bill",
  "description": "Make a payment for services rendered",
  "capabilities": ["make_payment", "view_invoice"]
}
```

## Output

Return a list of goal objects. Do NOT save to file - use pdf-goal-saver for that.
