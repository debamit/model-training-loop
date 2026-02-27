---
name: pdf-goal-extractor
description: Analyzes PDF documents to extract possible user goals and intents the bot can fulfill
trigger: analyze pdf, extract goals from pdf, pdf capabilities, what can i do with this pdf, pdf intent discovery
---

# PDF Goal Extractor

Analyzes a PDF document and extracts all possible user goals/intents based on its content.

## Goal File Location

**Goals are stored in:** `knowledge-base/pdf/<pdf_name>_goals.json`

Examples:
- Invoice PDF: `knowledge-base/pdf/invoice_goals.json`
- Contract PDF: `knowledge-base/pdf/contract_goals.json`
- Manual PDF: `knowledge-base/pdf/manual_goals.json`

To find all available goal files, use: `knowledge-base/pdf/*_goals.json`

## Step 1: Get the PDF

Ask user for:
- File path to PDF - use absolute path from working directory `/home/debamit007/model-training-loop`
- Or ask "Where is the PDF located?"

If user says "figure it out", check common locations:
- Current directory
- `knowledge-base/pdf/`
- `documents/`
- Use `glob` to find `*.pdf`

## Step 2: Read and Analyze the PDF

Use Python with pdfplumber (recommended) or pypdf2:

```python
import pdfplumber

with pdfplumber.open('/path/to/file.pdf') as pdf:
    text = ''
    for page in pdf.pages[:10]:  # First 10 pages
        text += page.extract_text() or ''
```

Or with PyPDF2:
```python
import PyPDF2
with open('/path/to/file.pdf', 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    text = ''
    for page in reader.pages[:10]:
        text += page.extract_text()
```

## Step 3: Map Content to User Goals

Analyze the PDF content and think from a USER'S perspective - what would someone want to accomplish with this document?

| Document Type | Possible User Goals |
|---------------|---------------------|
| Invoice | "Pay my bill", "View charges", "Download receipt", "Dispute a charge" |
| Contract | "Sign the contract", "Review terms", "Check obligations" |
| Manual | "Learn how to use X", "Find troubleshooting steps", "Get setup instructions" |
| Report | "Summarize findings", "Extract key metrics", "Compare to previous" |
| Form | "Fill out the form", "Submit application", "Check requirements" |

The user goal should be:
- In natural language ("Pay my bill", "Check my order status")
- Something a non-technical person would say
- Focused on the outcome, not the mechanism

## Step 4: Save Goals to File

Generate filename from PDF name by appending `_goals.json`:
- `invoice.pdf` → `knowledge-base/pdf/invoice_goals.json`
- `contract.pdf` → `knowledge-base/pdf/contract_goals.json`
- `manual.pdf` → `knowledge-base/pdf/manual_goals.json`

**Location hint:** Always save to `knowledge-base/pdf/` directory (relative to the current working directory where the skill is run).

Save format:
```json
{
  "source": "<pdf_path>",
  "location": "knowledge-base/pdf/<pdf_name>_goals.json",
  "document_type": "<type of document>",
  "goals": [
    {
      "id": 1,
      "user_goal": "<user-friendly goal>",
      "description": "<what this goal accomplishes>",
      "capabilities": ["<related feature or action>"]
    }
  ],
  "simulated": [],
  "last_updated": "<YYYY-MM-DD>"
}
```

## Step 5: Present Goals to User

Format the extracted goals from the USER'S perspective:

```markdown
## What You Can Do With This Document

Based on the PDF analysis, here are things you can accomplish:

1. **<Goal 1>** - <description>
2. **<Goal 2>** - <description>
...
```

## PDF Processing Tips

- Available libraries: `pdfplumber` ✓
- For scanned PDFs, you may need OCR (use `pytesseract` or online services)
- If PDF is image-heavy, try `pdfplumber` for better extraction
- Check file size - very large PDFs may need chunked processing
- Ask user if they want goals from specific sections or the full document
