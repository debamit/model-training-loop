---
name: api-spec-finder
description: Find API specification files (OpenAPI/Swagger JSON/YAML)
trigger: find api spec, locate api spec, where is api spec, search api spec
---

# API Spec Finder

Find API specification files in common locations.

## Locations

Check these directories (relative to working dir):
- `specs/`
- Current directory

## Code

```python
from glob import glob

patterns = ['specs/*.json', 'specs/*.yaml', 'specs/*.yml', '*.json']
files = []
for pattern in patterns:
    files.extend(glob(pattern))
return files
```

## Output

Return list of found API spec file paths.
