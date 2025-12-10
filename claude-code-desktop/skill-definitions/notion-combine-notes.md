---
name: notion-combine-notes
description: Combine multiple Notion notes into one. Use when the user wants to merge, consolidate, or combine content from multiple notes into a single note in the Ultimate Brain system.
---

# Combine Notes in Notion

Combine content from multiple notes into a single note. Supports appending to an existing note or creating a new combined note. Source notes are automatically archived after successful combination.

## When to Use

Use this Skill when the user wants to:
- Merge multiple related notes into one master note
- Consolidate meeting notes from different sessions
- Combine research notes from various sources
- Create a summary note from multiple individual notes

## How to Execute

### Append to Existing Note

Combine multiple source notes and append their content to an existing target note:

```bash
python3 ~/.claude/scripts/notion/combine_notes.py \
  --source-ids "SOURCE_ID_1" "SOURCE_ID_2" "SOURCE_ID_3" \
  --target-id "TARGET_NOTE_ID"
```

### Create New Combined Note

Combine multiple source notes into a brand new note:

```bash
python3 ~/.claude/scripts/notion/combine_notes.py \
  --source-ids "SOURCE_ID_1" "SOURCE_ID_2" \
  --create-new "Combined Meeting Notes - Q1 2024"
```

### Advanced Options

Disable title preservation (don't add source note titles as headings):

```bash
python3 ~/.claude/scripts/notion/combine_notes.py \
  --source-ids "ID1" "ID2" \
  --create-new "New Note" \
  --no-preserve-titles
```

Don't archive source notes after combining:

```bash
python3 ~/.claude/scripts/notion/combine_notes.py \
  --source-ids "ID1" "ID2" \
  --target-id "TARGET_ID" \
  --no-archive
```

Don't add dividers between notes:

```bash
python3 ~/.claude/scripts/notion/combine_notes.py \
  --source-ids "ID1" "ID2" \
  --create-new "New Note" \
  --no-separator
```

## Default Behavior

By default, the script:
1. **Preserves source titles**: Adds each source note's title as a Heading 2
2. **Archives sources**: Automatically archives all source notes after successful combination
3. **Adds separators**: Inserts divider lines between combined notes
4. **Limits to 5 notes**: Maximum 5 notes can be combined in one operation

## How Content is Combined

1. For each source note in order:
   - Adds source note title as Heading 2 (if preserve_titles=True)
   - Copies all content blocks from that note
   - Adds a divider (if separator=True and not the last note)

2. Supported block types:
   - Paragraphs, headings (H1, H2, H3)
   - Bulleted lists, numbered lists, to-do lists
   - Code blocks (with language preservation)
   - Quotes, callouts, toggles
   - Dividers
   - External images (hosted images only)

3. Unsupported block types (skipped):
   - Child pages, databases
   - Embeds, bookmarks
   - Files, PDFs

## Technical Notes

### No Bash Argument Limits

This script avoids bash command-line argument length limits by:
- Reading content directly via Notion API
- Combining blocks in Python memory
- Sending blocks directly to Notion API (not through bash arguments)

This means you can combine notes of any size without hitting shell limits.

### Rate Limiting

The script respects Notion API rate limits:
- 0.3 second delay between API calls
- Safe to combine up to 5 notes in one operation

### Automatic Source Archiving

After successful combination, source notes are automatically archived. This:
- Keeps your workspace clean
- Preserves source notes (they're archived, not deleted)
- Can be disabled with `--no-archive` flag

## Workflow Examples

### Combine Weekly Meeting Notes

User: "Combine my three meeting notes from this week into one"

1. Use search-notes or list-project-notes to find the meeting notes
2. Extract the note IDs from results
3. Ask user: append to existing note or create new one?
4. Execute combine with appropriate parameters
5. Confirm: "Combined 3 notes into '[Note Name]'. Source notes have been archived."

### Consolidate Research Notes

User: "Merge all my API research notes into a master document"

1. Search for API research notes
2. Present matches (up to 5 at a time)
3. Execute combine into new note: "API Research - Master Document"
4. Report success and provide link to new note

## Error Handling

- **Too many sources**: Maximum 5 notes per operation (prevents overwhelming API)
- **No content found**: At least one source must have content
- **Invalid note IDs**: Clear error if any source note doesn't exist
- **Both modes specified**: Can't use both `--target-id` and `--create-new`

## Safety Features

- Source notes are only archived AFTER successful combination
- If combination fails, source notes remain untouched
- Returns detailed result with all actions taken
- Archiving failures don't abort the operation (logged as warnings)

## Handling Results

- Confirm successful combination
- Report number of blocks combined
- List which source notes were archived
- Provide link to target/new note
- Offer to read the combined note to verify

## Example Interaction

User: "Combine notes A, B, and C into a new note called 'Master Summary'"
