---
name: notion-search-notes
description: Search for notes by keyword in Notion. Use when the user wants to find notes containing specific keywords or search within projects in the Ultimate Brain system.
---

# Search Notes in Notion

Search for notes in the Ultimate Brain Notion workspace by keyword.

## When to Use

Use this Skill when the user wants to:
- Find notes containing specific keywords
- Search within a specific project
- Locate notes they vaguely remember

## How to Execute

### Basic Search Across All Notes

```bash
python3 ~/.claude/scripts/notion/search_notes.py --query "SEARCH_TERM"
```

### Search Within a Specific Project

```bash
python3 ~/.claude/scripts/notion/search_notes.py --query "SEARCH_TERM" --project-name "PROJECT_NAME"
```

### Search With Project ID

```bash
python3 ~/.claude/scripts/notion/search_notes.py --query "SEARCH_TERM" --project-id "PROJECT_ID"
```

### Limit Results

```bash
python3 ~/.claude/scripts/notion/search_notes.py --query "SEARCH_TERM" --limit 5
```

## Search Behavior

- Search is **case-insensitive**
- Searches note **titles only** (not content)
- Partial matches are included (e.g., "serv" matches "Server", "Serveri")
- Archived notes are excluded by default

## Handling Results

- Parse the JSON output from the script
- Present matching notes with their IDs
- Suggest using `notion-read-note` skill to view full content

## Example Output Format for User

```
Found 3 notes matching "API":

1. API Integration Guide
   Project: Development
   ID: 12345678-1234-1234-1234-123456789abc

2. REST API Notes
   Project: Example Project
   ID: 87654321-4321-4321-4321-cba987654321

3. API Authentication
   Project: (none)
   ID: abcdef12-3456-7890-abcd-ef1234567890

Use the note ID with the notion-read-note skill to view full content.
```

## Important Notes

- Search only matches note titles, not content
- For content search, user would need to read notes and search manually
- Project name matching is also partial (e.g., "serv" finds "Serveri")
