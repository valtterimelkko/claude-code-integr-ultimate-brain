---
name: notion-edit-note
description: Edit content of a Notion note. Use when the user wants to add, replace, or clear content in an existing note in the Ultimate Brain system.
---

# Edit Note in Notion

Edit the content of notes in the Ultimate Brain Notion workspace. Supports appending new content, replacing all content, or clearing content.

## When to Use

Use this Skill when the user wants to:
- Add content to an existing note
- Replace note content entirely
- Clear a note's content

## How to Execute

**IMPORTANT**: The parameter is `--id` (NOT `--note-id`)

### Append Content (Default - Safest)

Add new content to the end of the note:

```bash
python3 ~/.claude/scripts/notion/edit_note.py --id "NOTE_ID" --action append --content "Content to add"
```

Or by name:
```bash
python3 ~/.claude/scripts/notion/edit_note.py --name "NOTE_NAME" --action append --content "Content to add"
```

### Replace Content (Destructive - Confirm First!)

Replace all content with new content:

```bash
python3 ~/.claude/scripts/notion/edit_note.py --id "NOTE_ID" --action replace --content "# New Content\n\nThis replaces everything."
```

### Clear Content (Destructive - Confirm First!)

Remove all content from the note:

```bash
python3 ~/.claude/scripts/notion/edit_note.py --id "NOTE_ID" --action clear
```

### Using Content File

For longer content, use a file:

```bash
python3 ~/.claude/scripts/notion/edit_note.py --id "NOTE_ID" --action append --content-file /tmp/content.txt
```

## Content Formatting

The script parses text content into Notion blocks:

| Markdown Syntax | Notion Block Type |
|-----------------|-------------------|
| `# Heading` | heading_1 |
| `## Heading` | heading_2 |
| `### Heading` | heading_3 |
| `- Item` or `* Item` | bulleted_list_item |
| `1. Item` | numbered_list_item |
| ` ```code``` ` | code block |
| Other text | paragraph |

## Safety Guidelines

**ALWAYS follow these rules:**

1. **For "append" action**: Safe to proceed without explicit confirmation
2. **For "replace" action**: ALWAYS confirm with user before executing
3. **For "clear" action**: ALWAYS confirm with user before executing

Ask: "This will permanently replace/clear all content in '[Note Name]'. Are you sure?"

## Handling Results

- Confirm the action was successful
- Report how many blocks were added/removed
- Offer to read the note to verify changes

## Example Interaction

User: "Add a new section to my API notes about rate limiting"

1. Use search-notes to find the note
2. Present the match and confirm which note to edit
3. Ask user for the content to add
4. Execute append action
5. Confirm success
