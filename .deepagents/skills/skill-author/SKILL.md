---
name: skill-author
description: Instructions for creating new DeepAgents skills. Use this whenever you need to create, modify, or understand skills in this project.
trigger: create skill, write skill, how to skill, new skill, skill author, skill creation
---

# Skill Author

You create skills for the DeepAgents CLI. A skill is a reusable agent capability defined entirely in a `SKILL.md` file.

## When to Create a Skill

Create a skill when you need the agent to:
- Have specialized domain knowledge
- Follow specific workflows
- Access custom data or templates
- Execute multi-step procedures consistently

## When NOT to Write Code

**Skills should be self-contained in SKILL.md.** Only write Python code if:
- You need to enforce a constraint the user explicitly provides
- The operation cannot be done with existing tools (read_file, write_file, shell, etc.)

Most tasks can be done with:
- `read_file` - Read existing files (JSON, markdown, etc.)
- `write_file` - Create/update files
- `shell` - Run commands
- Natural conversation - Ask user questions

## Skill File Structure

```
.deepagents/skills/<skill-name>/
└── SKILL.md
```

### Frontmatter (Required)

```yaml
---
name: skill-name
description: Brief description of what the skill does. This is used to match the skill to user requests.
trigger: trigger words that activate this skill
---
```

### Body

```
# Skill Name

## Overview
Brief description of what this skill does.

## Instructions
Step-by-step instructions for the agent to follow.

### Step 1
What to do

### Step 2
What to do

## Data Storage
Where data is stored (if any).

## Examples
Example interactions.
```

## Tools Available

The agent has these tools built-in:
- `ls` - List files
- `read_file` - Read file contents
- `write_file` - Create/overwrite files
- `edit_file` - Make targeted edits
- `glob` - Find files by pattern
- `grep` - Search in files
- `shell` - Execute commands

## Example: User Context Skill

Instead of writing Python, the skill instructs the agent to:

1. **Read** existing context with `read_file`:
   ```
   read_file user_context.json
   ```

2. **Update** by writing back:
   ```
   write_file user_context.json <updated-content>
   ```

3. **Ask questions** naturally to gather user information

## Creating a New Skill

1. Create directory: `.deepagents/skills/<skill-name>/`
2. Write `SKILL.md` with frontmatter + instructions
3. Update CHECKPOINT.md to document the new skill

## Key Principles

1. **K.I.S.S.** - Keep skills simple
2. **Self-contained** - Everything in SKILL.md
3. **Use existing tools** - Don't write code unless necessary
4. **Clear triggers** - Make description specific enough to match correctly
5. **Document data storage** - Always note where data lives (JSON, files, etc.)

## References

- DeepAgents Skills Docs: https://docs.langchain.com/oss/python/deepagents/skills
- Agent Skills Spec: https://agentskills.io/specification
