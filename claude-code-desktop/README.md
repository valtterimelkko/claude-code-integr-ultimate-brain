# Claude Code & Claude Desktop Integration

This folder contains all resources for integrating Ultimate Brain with **Claude Code** (VS Code extension) or **Claude Desktop** (native application).

## What's Inside

- **`scripts/`** - Python backend scripts that interact with the Notion API
- **`skill-definitions/`** - Claude Code skill definition files (SKILL.md)

## Setup Instructions

See the main [README.md](../README.md) in the repository root for complete installation and setup instructions.

### Quick Start

1. Copy `scripts/` to `~/.claude/scripts/notion/`
2. Copy `skill-definitions/*/SKILL.md` to `~/.claude/skills/notion-*/SKILL.md`
3. Configure your database IDs and Notion token as described in the main README

## Files Overview

### Scripts (`scripts/`)

- **`common.py`** - Shared utilities, API configuration, credential loading
- **`create_note.py`** - Create new notes in Notion
- **`edit_note.py`** - Edit existing note content
- **`list_project_notes.py`** - List all notes in a project
- **`read_note.py`** - Read full note content
- **`search_notes.py`** - Search notes by keyword
- **`search_projects.py`** - Find projects by name

### Skill Definitions (`skill-definitions/`)

- **`notion-create-note.md`** - Create note skill documentation
- **`notion-edit-note.md`** - Edit note skill documentation
- **`notion-list-project-notes.md`** - List project notes skill documentation
- **`notion-read-note.md`** - Read note skill documentation
- **`notion-search-notes.md`** - Search notes skill documentation

## Configuration

All scripts use configuration from:
- **Database IDs**: `scripts/common.py` (lines 22-23)
- **Notion Token**: `/etc/keep-to-notion/env.conf`

For detailed configuration instructions, see the main README.md.

## Compatibility

✅ **Claude Code** (VS Code extension)
✅ **Claude Desktop** (native application)
