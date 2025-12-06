---
name: notion-create-note
description: Create a new note in the Notion Note inbox. Use when the user wants to create a new note, capture ideas, or start a new document in the Ultimate Brain system.
---

# Create Note in Notion

Create a new note in the Ultimate Brain Notion workspace. Notes are created in the Notes database without any project relations, allowing you to manually connect them to projects in Notion.

## When to Use

Use this Skill when the user wants to:
- Create a new note with a title
- Capture quick ideas or information as separate pages
- Create a note and add initial content to it
- Start a new document in the Notion system

## How to Execute

### Create Note with Title Only

Create a minimal note with just a title:

```bash
python3 ~/.claude/scripts/notion/create_note.py --title "My New Note"
```

### Create Note with Content

Add content to the note when creating it:

```bash
python3 ~/.claude/scripts/notion/create_note.py --title "My New Note" --content "# Heading\n\nSome content here"
```

### Create Note with Content from File

For longer content, use a file:

```bash
python3 ~/.claude/scripts/notion/create_note.py --title "My New Note" --content-file /tmp/content.txt
```

## Content Formatting

The script parses text content into Notion blocks using markdown-like syntax:

| Markdown Syntax | Notion Block Type |
|-----------------|-------------------|
| `# Heading` | heading_1 |
| `## Heading` | heading_2 |
| `### Heading` | heading_3 |
| `- Item` or `* Item` | bulleted_list_item |
| `1. Item` | numbered_list_item |
| ` ```code``` ` | code block |
| Other text | paragraph |

## Note Inbox Pattern

Notes are created **unrelated to any project**. This is intentional because:

1. **Inbox pattern**: New notes land in a neutral inbox where you can review them
2. **User control**: You decide which project (if any) to link the note to
3. **Flexibility**: Avoids forcing Claude to guess project associations

You can manually relate the note to projects in Notion after creation.

## Default Properties

All notes are created with:

- **Name**: The title you provided
- **Archived**: `False` (not archived)
- **Project**: Empty (no initial project relation)

## Handling Results

- Return the note ID and URL so user can navigate to it
- Report how many content blocks were created
- Offer to add content or read it back to verify

## Example Interaction

User: "Create a note called 'API Design Notes'"

1. Execute create_note.py with the title
2. Return the note ID and link
3. Offer to add content or open in Notion

User: "Create a note about my meeting with specific content"

1. Gather the content from user
2. Execute create_note.py with both title and content
3. Confirm success and blocks created
4. Offer to relate it to a project
