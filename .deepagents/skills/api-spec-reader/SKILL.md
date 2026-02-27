---
name: api-spec-reader
description: Read and parse API specification files (OpenAPI/Swagger)
trigger: read api spec, parse api spec, get api spec content
---

# API Spec Reader

Read and parse an API specification file (JSON or YAML).

## Input

- API spec file path (JSON or YAML)

## Code

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
