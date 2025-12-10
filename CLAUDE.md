# Claude Code - Notion Skills Hub

## Your Role

This directory is the home for **Notion Claude Code skills** — a set of custom skills that enable efficient interaction with your Ultimate Brain Notion workspace. The skills provide structured, reliable access to your Notion databases through simple, context-efficient operations.

## Available Skills

Seven skills are available for use in Claude Code:

1. **[`notion-create-note`](/.claude/skills/notion-create-note/SKILL.md)** - Create a new note in the Note inbox
2. **[`notion-list-project-notes`](/.claude/skills/notion-list-project-notes/SKILL.md)** - List all notes in a specific project
3. **[`notion-search-notes`](/.claude/skills/notion-search-notes/SKILL.md)** - Search for notes by keyword
4. **[`notion-read-note`](/.claude/skills/notion-read-note/SKILL.md)** - Read the full content of a note
5. **[`notion-edit-note`](/.claude/skills/notion-edit-note/SKILL.md)** - Edit note content (append, replace, or clear)
6. **[`notion-archive-note`](/.claude/skills/notion-archive-note/SKILL.md)** - Archive or unarchive a note
7. **[`notion-combine-notes`](/.claude/skills/notion-combine-notes/SKILL.md)** - Combine multiple notes into one

## Architecture

The skills are built on a **script-based architecture** for reliability and context efficiency:

```
~/.claude/skills/
├── notion-archive-note/
│   └── SKILL.md
├── notion-combine-notes/
│   └── SKILL.md
├── notion-create-note/
│   └── SKILL.md
├── notion-edit-note/
│   └── SKILL.md
├── notion-list-project-notes/
│   └── SKILL.md
├── notion-read-note/
│   └── SKILL.md
└── notion-search-notes/
    └── SKILL.md

~/.claude/scripts/notion/           # Backend scripts
├── common.py                       # Shared utilities & API helpers
├── archive_note.py                 # Archive/unarchive note
├── combine_notes.py                # Combine multiple notes
├── create_note.py                  # Create new note
├── edit_note.py                    # Edit note content
├── list_project_notes.py           # List project notes
├── read_note.py                    # Read note content
├── search_notes.py                 # Search notes by keyword
└── search_projects.py              # Find projects by name
```

## How the Skills Work

Each skill invokes a corresponding Python script that:
- Loads credentials from `/etc/keep-to-notion/env.conf`
- Queries the Notion API v2022-06-28
- Returns structured JSON output
- Implements automatic filtering (excludes archived items by default)
- Respects rate limiting (0.3s delays between API calls)

## Key Capabilities

- **Structured Output**: All operations return JSON with guaranteed format
- **Archived Filtering**: Automatically excludes archived notes unless explicitly requested
- **Name Resolution**: Search for projects and notes by partial name match
- **Error Handling**: Clear, actionable error messages
- **Context Efficient**: Returns only needed data, doesn't overload your context window

## Target Databases

| Database | ID | Purpose |
|----------|-----|---------|
| Notes | `2bf45010-ad5d-816a-8e25-f1f4d80a12a7` | Primary note storage |
| Projects | `2bf45010-ad5d-81c7-9372-e7de7a11a0df` | Project organization |

## Using the Skills

1. **In Claude Code**: Skills are automatically discovered and invoked when relevant (e.g., ask "Find notes about API design")
2. **How Claude executes them**: Claude autonomously decides when to use a skill based on your request and the skill's description
3. **Results**: Claude parses JSON output from backend scripts and presents results to you in readable format

## When to Use These Skills vs. Claude.ai

- **Claude Code (these skills)**: Use for reliable, structured Notion operations with context efficiency
- **Claude.ai (native Notion MCP)**: Use for conversational, exploratory Notion queries

## Technical Details

- **Python version**: 3.7+
- **Dependencies**: `requests` library
- **Credentials**: Loaded from `/etc/keep-to-notion/env.conf`
- **API Rate Limit**: Respects 3 requests/second with built-in delays
- **Archived Filter**: Property name `Archived`, checkbox type, default `False`

## Maintenance & Extending

To add a new skill following Anthropic's conventions:

1. Create a Python script in `/root/notion/scripts/skills/`
2. Import and use utilities from `common.py`
3. Ensure JSON output with `output_success()` or `output_error()`
4. Create a skill directory: `~/.claude/skills/notion-{action-name}/`
5. Create `SKILL.md` inside with proper YAML frontmatter:
   ```yaml
   ---
   name: notion-{action-name}
   description: Brief description of what this skill does and when to use it
   ---
   ```
6. Keep skill documentation under 500 lines

For bugfixes or improvements to existing scripts, update the corresponding `.py` file directly; skill documentation will remain unchanged unless behavior changes.

---

**Last updated**: 2025-12-10
**Skills created**: 7 (create-note, list-project-notes, search-notes, read-note, edit-note, archive-note, combine-notes)
**Skill scripts**: 9 (common.py + 8 feature scripts)
