---
name: api-spec-handler
description: Find and read API specification files (OpenAPI/Swagger JSON/YAML)
trigger: find api spec, locate api spec, where is api spec, search api spec, read api spec, parse api spec, get api spec content
---

# API Spec Handler

Find and read an API specification file in one step.

## Step 1: Find the spec file

Check these directories:
- `specs/`
- Current directory

```python
from glob import glob

patterns = ['specs/*.json', 'specs/*.yaml', 'specs/*.yml', '*.json']
files = []
for pattern in patterns:
    files.extend(glob(pattern))
```

If multiple files found, ask user which one to use.

## Step 2: Read and parse the spec

```python
import json
import yaml

def read_api_spec(path: str) -> dict:
    with open(path, 'r') as f:
        if path.endswith('.yaml') or path.endswith('.yml'):
            return yaml.safe_load(f)
        return json.load(f)
```

## Output

Return parsed spec as dict. Print endpoint count for verification.
