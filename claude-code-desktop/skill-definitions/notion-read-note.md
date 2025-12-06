---
name: notion-read-note
description: Read the full content of a Notion note. Use when the user wants to view or access note content by ID or name from the Ultimate Brain system.
---

# Read Note from Notion

Read the complete content of a note from the Ultimate Brain Notion workspace.

## When to Use

Use this Skill when the user wants to:
- View the full content of a note
- Read a note after finding it with search
- Access note content by ID (e.g., copied from Notion URL)

## How to Execute

### Read by Note ID (Preferred, Most Reliable)

**IMPORTANT**: The parameter is `--id` (NOT `--note-id`)

```bash
python3 ~/.claude/scripts/notion/read_note.py --id "NOTE_ID"
```

### Read by Note Name

```bash
python3 ~/.claude/scripts/notion/read_note.py --name "NOTE_NAME"
```

### Read by Name Within Specific Project (More Precise)

```bash
python3 ~/.claude/scripts/notion/read_note.py --name "NOTE_NAME" --project-name "PROJECT_NAME"
```

### Get Text-Only Output

```bash
python3 ~/.claude/scripts/notion/read_note.py --id "NOTE_ID" --format text-only
```

### Read Multiple Notes Efficiently

**IMPORTANT**: When reading multiple notes (e.g., after listing project notes), run commands in PARALLEL using multiple Bash tool calls in a single message. Do NOT chain with `&&`.

**Rate Limit Safety**: Notion API allows 3 requests/second average with burst tolerance. Reading 5-20 notes in parallel is safe and recommended. For 20+ notes, consider processing in batches of 15-20.

Example - CORRECT approach (parallel):
```
Use multiple Bash tool calls in one message:
- Bash call 1: python3 ~/.claude/scripts/notion/read_note.py --id "NOTE_ID_1"
- Bash call 2: python3 ~/.claude/scripts/notion/read_note.py --id "NOTE_ID_2"
- Bash call 3: python3 ~/.claude/scripts/notion/read_note.py --id "NOTE_ID_3"
... up to 15-20 notes per batch
```

Example - WRONG approach (sequential):
```bash
# Don't do this - it's slow and inefficient
python3 ~/.claude/scripts/notion/read_note.py --id "ID_1" && \
python3 ~/.claude/scripts/notion/read_note.py --id "ID_2" && \
python3 ~/.claude/scripts/notion/read_note.py --id "ID_3"
```

## Handling Results

- Parse the JSON output
- Present the note content in a readable format
- For code blocks, preserve formatting with syntax highlighting hints

## Example Output Format for User

```
# API Integration Guide
Project: Development
Last updated: March 20, 2024

---

## Overview

This guide covers how to integrate with our API...

## Authentication

Use bearer tokens for authentication:

\`\`\`python
headers = {"Authorization": f"Bearer {token}"}
\`\`\`

- Step 1: Get your API key
- Step 2: Include it in headers
- Step 3: Make requests

---
```

## Important Notes

- If searching by name returns multiple matches, ask user to be more specific or use the ID
- Note IDs can be extracted from Notion URLs: notion.so/Note-Title-**NOTE_ID_HERE**
- Archived notes can still be read by ID but won't appear in name searches
