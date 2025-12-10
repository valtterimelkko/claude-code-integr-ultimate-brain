---
name: notion-archive-note
description: Archive or unarchive a Notion note. Use when the user wants to archive a note (mark as archived) or unarchive it in the Ultimate Brain system.
---

# Archive Note in Notion

Archive or unarchive notes in the Ultimate Brain Notion workspace by toggling the `Archived` checkbox property.

## When to Use

Use this Skill when the user wants to:
- Archive a note they no longer need active
- Mark a note as archived/completed
- Unarchive a note they want to restore (less common)

## How to Execute

**IMPORTANT**: The parameter is `--id` (NOT `--note-id`)

### Archive a Note (Default)

Archive by ID:

```bash
python3 ~/.claude/scripts/notion/archive_note.py --id "NOTE_ID"
```

Archive by name:

```bash
python3 ~/.claude/scripts/notion/archive_note.py --name "NOTE_NAME"
```

Archive by name within specific project:

```bash
python3 ~/.claude/scripts/notion/archive_note.py --name "NOTE_NAME" --project-name "PROJECT_NAME"
```

### Unarchive a Note

Restore an archived note:

```bash
python3 ~/.claude/scripts/notion/archive_note.py --id "NOTE_ID" --action unarchive
```

Or by name:

```bash
python3 ~/.claude/scripts/notion/archive_note.py --name "NOTE_NAME" --action unarchive
```

## Understanding Archived Status

In the Ultimate Brain system:
- **Archived notes** have the `Archived` checkbox property set to `True`
- Archived notes are excluded from most searches and listings by default
- Archiving is NOT the same as Notion's built-in archive feature
- This is a soft delete - notes remain accessible but hidden from active views

## Safety Features

- If note is already in the desired state (archived/unarchived), returns success with "no_change" status
- Returns clear error if note not found
- For name-based search, prompts for clarification if multiple matches found

## Handling Results

- Confirm the action was successful
- Report the note name and new archived status
- If "no_change" status, inform user the note was already in that state

## Example Interactions

**User: "Archive my meeting notes from last week"**

1. Use search-notes to find the meeting notes
2. Present the match and confirm which note to archive
3. Execute archive action
4. Confirm success: "Note '[Note Name]' has been archived"

**User: "I accidentally archived the wrong note, can you unarchive it?"**

1. Ask for note name or ID
2. Execute unarchive action
3. Confirm success: "Note '[Note Name]' has been unarchived"

## Common Workflows

### Archive After Combining Notes

When combining multiple notes into one (see combine-notes skill), the source notes are automatically archived. You don't need to manually archive them in that workflow.

### Batch Archiving

This skill archives one note at a time. For batch archiving based on criteria (age, project, etc.), the user has separate automation workflows.

## Notes

- Unarchiving is available but primarily used for mistakes/restoration
- Default action is always "archive" - you must explicitly specify `--action unarchive`
- Archived notes can still be read by ID using the read-note skill
- When searching for notes to unarchive, use `--action unarchive` to include archived notes in the search
