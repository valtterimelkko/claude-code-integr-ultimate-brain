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

### Using Content File (REQUIRED for Long Content)

**CRITICAL: For content longer than a few paragraphs (>500 characters), you MUST use --content-file instead of --content.**

Bash command-line arguments have length limits. Using `--content` with long text will fail or truncate content. Always use a temporary file for substantial content:

```bash
python3 ~/.claude/scripts/notion/edit_note.py --id "NOTE_ID" --action append --content-file /tmp/content.txt
```

**Best Practice Workflow:**

1. Write the content to a temporary file using the Write tool
2. Use `--content-file` parameter pointing to that file
3. The script will read the file directly (no bash limits)

Example:

```bash
# First: Create temp file with Write tool
# /tmp/notion_content_12345.txt contains your full content

# Then: Execute edit with --content-file
python3 ~/.claude/scripts/notion/edit_note.py --id "NOTE_ID" --action append --content-file /tmp/notion_content_12345.txt
```

**When to Use Each Method:**

- `--content "Short text"`: Only for brief content (< 500 characters, ~3-4 sentences)
- `--content-file /tmp/file.txt`: For any substantial content (paragraphs, articles, long notes)

**IMPORTANT**: Never summarize or truncate content to fit `--content` limits. If the user provides or requests long content, ALWAYS use the file-based approach.

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
