#!/usr/bin/env python3
"""
Create a new note in the Note Inbox of the Ultimate Brain system.

This script creates a new note page in the Notes database with a given title
and optional initial content. The note is created unrelated to any project,
allowing the user to manually connect it to projects in Notion.
"""

import argparse
import requests
import sys
import time
from common import (
    NOTES_DB_ID, NOTION_BASE_URL, get_headers,
    output_success, output_error
)

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
        import re
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

def create_note(title, content=None, content_file=None):
    """
    Create a new note in the Notes database.

    Args:
        title: Title of the note (required)
        content: Optional content to add to the note
        content_file: Path to file with content
    """
    if not title or not title.strip():
        output_error("Title is required")

    headers = get_headers()

    # Get content from file or argument
    if content_file:
        try:
            with open(content_file, 'r') as f:
                content = f.read()
        except Exception as e:
            output_error(f"Failed to read content file: {str(e)}")

    # Parse content into blocks if provided
    children = []
    if content:
        children = parse_markdown_to_blocks(content)

    # Build page creation payload
    page_data = {
        "parent": {
            "database_id": NOTES_DB_ID
        },
        "properties": {
            "Name": {
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": title.strip()
                        }
                    }
                ]
            },
            "Archived": {
                "checkbox": False
            }
        }
    }

    # Add children (content blocks) if any
    if children:
        page_data["children"] = children

    # Create the page
    url = f"{NOTION_BASE_URL}/pages"

    try:
        response = requests.post(url, headers=headers, json=page_data, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        output_error(f"API request failed: {str(e)}")

    page = response.json()
    note_id = page.get('id')

    output_success({
        "action": "create",
        "note": {
            "id": note_id,
            "name": title.strip(),
            "url": page.get('url', '')
        },
        "content": {
            "blocks_created": len(children)
        }
    })

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a new note in the Ultimate Brain Notes database"
    )
    parser.add_argument("--title", required=True, help="Title of the new note")
    parser.add_argument("--content", help="Optional content to add to the note")
    parser.add_argument("--content-file", help="Path to file with content")

    args = parser.parse_args()

    create_note(
        title=args.title,
        content=args.content,
        content_file=args.content_file
    )
