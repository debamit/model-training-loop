---
name: pdf-reader
description: Extract text content from a PDF file
trigger: read pdf, extract pdf text, get pdf content, pdf to text
---

# PDF Reader

Extract text from a PDF file.

## Input

- PDF file path (absolute path from `/home/debamit007/model-training-loop`)

## Code

Use pdfplumber (recommended):

```python
import pdfplumber

def read_pdf(pdf_path: str, max_pages: int = 10) -> str:
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages[:max_pages]:
            text += page.extract_text() or ''
        return text
```

Or PyPDF2:

```python
import PyPDF2

def read_pdf(pdf_path: str, max_pages: int = 10) -> str:
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ''
        for page in reader.pages[:max_pages]:
            text += page.extract_text() or ''
        return text
```

## Output

Return the extracted text. Print page count for verification.
