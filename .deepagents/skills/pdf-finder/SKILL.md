---
name: pdf-finder
description: Find PDF files in common locations
trigger: find pdf, locate pdf, where is my pdf, search pdf, pdf location
---

# PDF Finder

Find PDF files in common locations.

## Step 1: Ask for filename (optional)

If user specifies a filename, use it. Otherwise search broadly.

## Step 2: Search common locations

Check these directories (working dir: current directory):
- Current directory
- `knowledge-base/pdf/`
- `documents/`
- `downloads/`

## Step 3: Use glob to find PDFs

```python
from glob import glob

patterns = [
    '**/*.pdf',              # everywhere
    'knowledge-base/pdf/*.pdf',
    'documents/*.pdf'
]

for pattern in patterns:
    files = glob(pattern, recursive=True)
    if files:
        return files
```

## Step 4: Return found paths

Return absolute paths to found PDFs.
