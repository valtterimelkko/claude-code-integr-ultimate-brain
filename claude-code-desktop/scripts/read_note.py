#!/usr/bin/env python3
"""
Read the full content of a Notion note.

This script fetches a note's metadata and content blocks, returning them in JSON format.
"""

import argparse
import requests
import sys
import subprocess
import json
import time
from common import (
    NOTES_DB_ID, NOTION_BASE_URL, get_headers,
    build_title_filter, build_project_filter, build_archived_filter, combine_filters,
    output_success, output_error, extract_title, extract_block_text
)

def get_project_name_from_id(project_id):
    """Get project name from ID by fetching the page."""
    headers = get_headers()
    url = f"{NOTION_BASE_URL}/pages/{project_id}"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            page = response.json()
            return extract_title(page)
    except:
        pass

    return None

def find_note_by_name(note_name, project_name=None):
    """
    Find a note by name (and optionally by project).

    Args:
        note_name: Name of the note to find
        project_name: Optional project name to limit search

    Returns:
        str: Note ID

    Raises:
        SystemExit: If note not found or multiple matches
    """
    # Build search query
    headers = get_headers()
    title_filter = build_title_filter(note_name)

    # If project name provided, resolve it first
    project_id = None
    if project_name:
        import os
        # Try to locate the search_projects.py script
        script_path = "~/.claude/scripts/notion/search_projects.py"
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

def get_note_content(note_id):
    """
    Get full content blocks of a note.

    Args:
        note_id: Note ID

    Returns:
        list: List of block objects
    """
    headers = get_headers()
    url = f"{NOTION_BASE_URL}/blocks/{note_id}/children"
    blocks = []

    try:
        while True:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            data = response.json()
            blocks.extend(data.get('results', []))

            # Check for pagination
            if not data.get('has_more', False):
                break

            # Get next page
            url = f"{NOTION_BASE_URL}/blocks/{note_id}/children?start_cursor={data.get('next_cursor')}"
            time.sleep(0.3)  # Rate limiting
    except requests.exceptions.RequestException as e:
        output_error(f"Failed to fetch note content: {str(e)}")

    return blocks

def read_note(note_id=None, note_name=None, project_name=None, format="full"):
    """
    Read a note's content.

    Args:
        note_id: Note ID (if not provided, note_name is required)
        note_name: Note name to search for
        project_name: Optional project name to limit search
        format: Output format ("full", "text-only", or "summary")
    """
    # Resolve note name to ID if needed
    if note_name and not note_id:
        note_id = find_note_by_name(note_name, project_name)

    if not note_id:
        output_error("Either --id or --name must be provided")

    headers = get_headers()

    # Get note metadata
    url = f"{NOTION_BASE_URL}/pages/{note_id}"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        output_error(f"Failed to fetch note: {str(e)}")

    page = response.json()
    note_title = extract_title(page)

    # Get project if assigned
    note_project = None
    project_prop = page.get('properties', {}).get('Project', {})
    if project_prop.get('type') == 'relation':
        relations = project_prop.get('relation', [])
        if relations:
            note_project_id = relations[0].get('id')
            note_project = get_project_name_from_id(note_project_id)

    # Get content blocks
    blocks = get_note_content(note_id)

    # Format output based on requested format
    if format == "text-only":
        # Convert blocks to markdown-like text
        text_lines = []
        for block in blocks:
            block_data = extract_block_text(block)
            block_text = block_data.get('text', '')
            if block_data.get('type') == 'heading_1':
                text_lines.append(f"# {block_text}")
            elif block_data.get('type') == 'heading_2':
                text_lines.append(f"## {block_text}")
            elif block_data.get('type') == 'heading_3':
                text_lines.append(f"### {block_text}")
            elif block_data.get('type') == 'code':
                language = block_data.get('language', 'plain text')
                text_lines.append(f"```{language}\n{block_text}\n```")
            elif block_data.get('type') == 'bulleted_list_item':
                text_lines.append(f"- {block_text}")
            elif block_data.get('type') == 'numbered_list_item':
                text_lines.append(f"1. {block_text}")
            elif block_data.get('type') == 'divider':
                text_lines.append("---")
            elif block_text:
                text_lines.append(block_text)

        output_success({
            "note": {
                "id": note_id,
                "name": note_title
            },
            "content": {
                "text": "\n\n".join(text_lines)
            }
        })

    elif format == "summary":
        # Get first 500 characters
        text_lines = []
        for block in blocks:
            block_data = extract_block_text(block)
            block_text = block_data.get('text', '')
            if block_text:
                text_lines.append(block_text)

        full_text = " ".join(text_lines)
        summary = full_text[:500] + ("..." if len(full_text) > 500 else "")

        output_success({
            "note": {
                "id": note_id,
                "name": note_title,
                "project": note_project
            },
            "content": {
                "summary": summary
            }
        })

    else:  # format == "full"
        # Return full block structure
        formatted_blocks = []
        for block in blocks:
            block_data = extract_block_text(block)
            formatted_blocks.append(block_data)

        output_success({
            "note": {
                "id": note_id,
                "name": note_title,
                "project": note_project,
                "created": page.get('created_time'),
                "updated": page.get('last_edited_time'),
                "archived": page.get('archived', False)
            },
            "content": {
                "block_count": len(formatted_blocks),
                "blocks": formatted_blocks
            }
        })

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Read the full content of a note"
    )
    parser.add_argument("--id", help="Note ID to read")
    parser.add_argument("--name", help="Note name to search for")
    parser.add_argument("--project-name", help="Optional project name for name search")
    parser.add_argument("--format", choices=["full", "text-only", "summary"], default="full",
                        help="Output format")

    args = parser.parse_args()

    if not args.id and not args.name:
        output_error("Either --id or --name must be provided")

    read_note(
        note_id=args.id,
        note_name=args.name,
        project_name=args.project_name,
        format=args.format
    )
