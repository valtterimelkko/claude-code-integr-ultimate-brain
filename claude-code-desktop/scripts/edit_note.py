#!/usr/bin/env python3
"""
Edit the content of a Notion note.

This script allows appending, replacing, or clearing note content.
"""

import argparse
import requests
import sys
import subprocess
import json
import time
import re
from common import (
    NOTES_DB_ID, NOTION_BASE_URL, get_headers,
    build_title_filter, build_project_filter, build_archived_filter, combine_filters,
    output_success, output_error, extract_title
)

def find_note_by_name(note_name, project_name=None):
    """
    Find a note by name (and optionally by project).

    Args:
        note_name: Name of the note to find
        project_name: Optional project name to limit search

    Returns:
        str: Note ID
    """
    headers = get_headers()
    title_filter = build_title_filter(note_name)

    # If project name provided, resolve it first
    project_id = None
    if project_name:
        import os
        # Try to locate the search_projects.py script
        script_path = "/root/.claude/scripts/notion/search_projects.py"
        if not os.path.exists(script_path):
            fallback_paths = [
                "/root/notion/scripts/skills/search_projects.py",
                os.path.expanduser("~/.claude/scripts/notion/search_projects.py")
            ]
            for path in fallback_paths:
                if os.path.exists(path):
                    script_path = path
                    break

        try:
            result = subprocess.run(
                ["python3", script_path,
                 "--name", project_name, "--limit", "1"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                if data['success']:
                    project_id = data['data']['projects'][0]['id']
        except:
            pass

    project_filter = build_project_filter(project_id) if project_id else None
    archived_filter = build_archived_filter(include_archived=False)
    combined_filter = combine_filters(title_filter, archived_filter, project_filter)

    body = {"page_size": 20}
    if combined_filter:
        body["filter"] = combined_filter

    url = f"{NOTION_BASE_URL}/databases/{NOTES_DB_ID}/query"

    try:
        response = requests.post(url, headers=headers, json=body, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        output_error(f"API request failed: {str(e)}")

    results = response.json().get('results', [])

    if not results:
        output_error(f"No notes found matching '{note_name}'")

    # Check for exact match
    exact_matches = [r for r in results if extract_title(r).lower() == note_name.lower()]
    if exact_matches:
        return exact_matches[0]['id']

    # If multiple matches, ask for clarification
    if len(results) > 1:
        matches = [extract_title(r) for r in results[:5]]
        output_error(
            f"Multiple notes match '{note_name}'. Please be more specific:",
            {"matches": matches}
        )

    return results[0]['id']

def parse_markdown_to_blocks(content):
    """
    Parse markdown-like text into Notion blocks.

    Args:
        content: Text content to parse

    Returns:
        list: List of block objects
    """
    blocks = []
    lines = content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check for code block
        if line.strip().startswith('```'):
            language = line.strip()[3:].strip() or 'plain text'
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            i += 1  # Skip closing ```

            blocks.append({
                "object": "block",
                "type": "code",
                "code": {
                    "rich_text": [{"type": "text", "text": {"content": '\n'.join(code_lines)}}],
                    "language": language
                }
            })
            continue

        # Check for heading 1
        if line.startswith('# '):
            blocks.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                }
            })
            i += 1
            continue

        # Check for heading 2
        if line.startswith('## '):
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": line[3:]}}]
                }
            })
            i += 1
            continue

        # Check for heading 3
        if line.startswith('### '):
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": line[4:]}}]
                }
            })
            i += 1
            continue

        # Check for bulleted list
        if line.startswith('- ') or line.startswith('* '):
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                }
            })
            i += 1
            continue

        # Check for numbered list
        if re.match(r'^\d+\.\s', line):
            match = re.match(r'^\d+\.\s(.*)$', line)
            if match:
                blocks.append({
                    "object": "block",
                    "type": "numbered_list_item",
                    "numbered_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": match.group(1)}}]
                    }
                })
            i += 1
            continue

        # Check for divider
        if line.strip() in ('---', '***', '___'):
            blocks.append({
                "object": "block",
                "type": "divider",
                "divider": {}
            })
            i += 1
            continue

        # Otherwise, treat as paragraph (skip empty lines)
        if line.strip():
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": line}}]
                }
            })
        i += 1

    return blocks

def delete_all_blocks(note_id):
    """
    Delete all blocks from a note.

    Args:
        note_id: Note ID to clear
    """
    headers = get_headers()

    # Get all blocks
    url = f"{NOTION_BASE_URL}/blocks/{note_id}/children"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        output_error(f"Failed to fetch blocks: {str(e)}")

    blocks = response.json().get('results', [])

    # Delete each block
    for block in blocks:
        block_id = block['id']
        delete_url = f"{NOTION_BASE_URL}/blocks/{block_id}"
        try:
            response = requests.delete(delete_url, headers=headers, timeout=10)
            response.raise_for_status()
            time.sleep(0.3)  # Rate limiting
        except requests.exceptions.RequestException as e:
            output_error(f"Failed to delete block: {str(e)}")

def append_blocks(note_id, blocks):
    """
    Append blocks to a note.

    Args:
        note_id: Note ID to append to
        blocks: List of block objects to append

    Returns:
        int: Number of blocks added
    """
    headers = get_headers()
    url = f"{NOTION_BASE_URL}/blocks/{note_id}/children"

    blocks_added = 0

    # Notion API has a limit of 100 blocks per request
    for i in range(0, len(blocks), 100):
        chunk = blocks[i:i+100]
        body = {"children": chunk}

        try:
            response = requests.patch(url, headers=headers, json=body, timeout=10)
            response.raise_for_status()
            blocks_added += len(chunk)
            time.sleep(0.3)  # Rate limiting
        except requests.exceptions.RequestException as e:
            output_error(f"Failed to append blocks: {str(e)}")

    return blocks_added

def edit_note(note_id=None, note_name=None, project_name=None, action="append", content=None, content_file=None):
    """
    Edit a note's content.

    Args:
        note_id: Note ID (if not provided, note_name is required)
        note_name: Note name to search for
        project_name: Optional project name to limit search
        action: Edit action ("append", "replace", or "clear")
        content: Content to add
        content_file: Path to file with content
    """
    # Resolve note name to ID if needed
    if note_name and not note_id:
        note_id = find_note_by_name(note_name, project_name)

    if not note_id:
        output_error("Either --id or --name must be provided")

    # Get note metadata for response
    headers = get_headers()
    url = f"{NOTION_BASE_URL}/pages/{note_id}"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        output_error(f"Failed to fetch note: {str(e)}")

    page = response.json()
    note_title = extract_title(page)

    # Get content from file or argument
    if content_file:
        try:
            with open(content_file, 'r') as f:
                content = f.read()
        except Exception as e:
            output_error(f"Failed to read content file: {str(e)}")
    elif not content and action != "clear":
        output_error("Either --content or --content-file must be provided for this action")

    # Parse content into blocks
    blocks = parse_markdown_to_blocks(content) if content else []

    # Perform action
    blocks_added = 0
    blocks_removed = 0

    if action == "clear":
        delete_all_blocks(note_id)
        blocks_removed = -1  # We don't know exact count, but some were removed
        blocks_added = 0
    elif action == "replace":
        delete_all_blocks(note_id)
        blocks_removed = -1
        blocks_added = append_blocks(note_id, blocks)
    elif action == "append":
        blocks_added = append_blocks(note_id, blocks)
        blocks_removed = 0
    else:
        output_error(f"Unknown action: {action}")

    output_success({
        "action": action,
        "note": {
            "id": note_id,
            "name": note_title
        },
        "changes": {
            "blocks_added": blocks_added,
            "blocks_removed": blocks_removed if blocks_removed != -1 else "unknown"
        }
    })

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Edit the content of a note"
    )
    parser.add_argument("--id", help="Note ID to edit")
    parser.add_argument("--name", help="Note name to search for")
    parser.add_argument("--project-name", help="Optional project name for name search")
    parser.add_argument("--action", choices=["append", "replace", "clear"], default="append",
                        help="Edit action")
    parser.add_argument("--content", help="Content to add/replace")
    parser.add_argument("--content-file", help="Path to file with content")

    args = parser.parse_args()

    if not args.id and not args.name:
        output_error("Either --id or --name must be provided")

    edit_note(
        note_id=args.id,
        note_name=args.name,
        project_name=args.project_name,
        action=args.action,
        content=args.content,
        content_file=args.content_file
    )
