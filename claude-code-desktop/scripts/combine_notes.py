#!/usr/bin/env python3
"""
Combine multiple Notion notes into one.

This script reads multiple source notes, combines their content, and either
appends to an existing note or creates a new note. Source notes are
automatically archived after successful combination.
"""

import argparse
import requests
import sys
import time
import subprocess
import json
from common import (
    NOTES_DB_ID, NOTION_BASE_URL, get_headers,
    output_success, output_error, extract_title, extract_block_text
)

def read_note_content(note_id):
    """
    Read all content blocks from a note.

    Args:
        note_id: Note ID to read

    Returns:
        dict: {"title": str, "blocks": list}
    """
    headers = get_headers()

    # Get note metadata
    page_url = f"{NOTION_BASE_URL}/pages/{note_id}"
    try:
        response = requests.get(page_url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        output_error(f"Failed to fetch note {note_id}: {str(e)}")

    page = response.json()
    title = extract_title(page)

    # Get note blocks
    blocks_url = f"{NOTION_BASE_URL}/blocks/{note_id}/children?page_size=100"
    all_blocks = []

    try:
        while blocks_url:
            response = requests.get(blocks_url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            all_blocks.extend(data.get('results', []))

            # Handle pagination
            if data.get('has_more'):
                next_cursor = data.get('next_cursor')
                blocks_url = f"{NOTION_BASE_URL}/blocks/{note_id}/children?page_size=100&start_cursor={next_cursor}"
            else:
                blocks_url = None

            time.sleep(0.3)  # Rate limiting
    except requests.exceptions.RequestException as e:
        output_error(f"Failed to fetch blocks for note {note_id}: {str(e)}")

    return {
        "id": note_id,
        "title": title,
        "blocks": all_blocks
    }

def blocks_to_notion_format(blocks):
    """
    Convert block objects to the format needed for creating new blocks.

    Args:
        blocks: List of block objects from API

    Returns:
        list: List of block objects ready for creation
    """
    new_blocks = []

    for block in blocks:
        block_type = block.get('type')

        # Skip unsupported block types
        if block_type in ['child_page', 'child_database', 'unsupported', 'embed', 'bookmark', 'file', 'pdf']:
            continue

        # Handle different block types
        if block_type in ['paragraph', 'heading_1', 'heading_2', 'heading_3',
                          'bulleted_list_item', 'numbered_list_item', 'to_do',
                          'toggle', 'quote', 'callout']:
            block_data = block.get(block_type, {})
            rich_text = block_data.get('rich_text', [])
            new_block = {
                "object": "block",
                "type": block_type,
                block_type: {
                    "rich_text": rich_text
                }
            }
            # Preserve special properties
            if block_type == 'to_do':
                new_block[block_type]['checked'] = block_data.get('checked', False)
            if block_type == 'code':
                new_block[block_type]['language'] = block_data.get('language', 'plain text')

            new_blocks.append(new_block)

        elif block_type == 'code':
            code_data = block.get('code', {})
            new_blocks.append({
                "object": "block",
                "type": "code",
                "code": {
                    "rich_text": code_data.get('rich_text', []),
                    "language": code_data.get('language', 'plain text')
                }
            })

        elif block_type == 'divider':
            new_blocks.append({
                "object": "block",
                "type": "divider",
                "divider": {}
            })

        elif block_type == 'image':
            # Images are tricky - we'll preserve external images only
            image_data = block.get('image', {})
            external_url = image_data.get('external', {}).get('url')
            if external_url:
                new_blocks.append({
                    "object": "block",
                    "type": "image",
                    "image": {
                        "type": "external",
                        "external": {"url": external_url}
                    }
                })

    return new_blocks

def create_title_block(title_text):
    """
    Create a heading_2 block for a note title.

    Args:
        title_text: Title to use

    Returns:
        dict: Block object
    """
    return {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": title_text}}]
        }
    }

def create_divider_block():
    """
    Create a divider block.

    Returns:
        dict: Block object
    """
    return {
        "object": "block",
        "type": "divider",
        "divider": {}
    }

def append_blocks_to_note(note_id, blocks):
    """
    Append blocks to an existing note.

    Args:
        note_id: Target note ID
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
            response = requests.patch(url, headers=headers, json=body, timeout=30)
            response.raise_for_status()
            blocks_added += len(chunk)
            time.sleep(0.3)  # Rate limiting
        except requests.exceptions.RequestException as e:
            output_error(f"Failed to append blocks: {str(e)}")

    return blocks_added

def create_new_note(title, blocks):
    """
    Create a new note with given blocks.

    Args:
        title: Note title
        blocks: List of block objects

    Returns:
        dict: Created note info
    """
    headers = get_headers()
    url = f"{NOTION_BASE_URL}/pages"

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
                            "content": title
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
    # Note: API limit is 100 children in creation, need to handle excess separately
    initial_blocks = blocks[:100]
    remaining_blocks = blocks[100:]

    if initial_blocks:
        page_data["children"] = initial_blocks

    # Create the page
    try:
        response = requests.post(url, headers=headers, json=page_data, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        output_error(f"Failed to create note: {str(e)}")

    page = response.json()
    note_id = page.get('id')

    # Append remaining blocks if any
    blocks_added = len(initial_blocks)
    if remaining_blocks:
        blocks_added += append_blocks_to_note(note_id, remaining_blocks)

    return {
        "id": note_id,
        "name": title,
        "url": page.get('url', ''),
        "blocks_created": blocks_added
    }

def archive_note(note_id):
    """
    Archive a note by setting Archived property to True.

    Args:
        note_id: Note ID to archive
    """
    headers = get_headers()
    url = f"{NOTION_BASE_URL}/pages/{note_id}"

    update_data = {
        "properties": {
            "Archived": {
                "checkbox": True
            }
        }
    }

    try:
        response = requests.patch(url, headers=headers, json=update_data, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Don't fail the whole operation if archiving fails
        print(f"Warning: Failed to archive note {note_id}: {str(e)}", file=sys.stderr)

def combine_notes(source_ids, target_id=None, new_note_title=None,
                  preserve_titles=True, archive_sources=True, separator=True):
    """
    Combine multiple notes into one.

    Args:
        source_ids: List of source note IDs
        target_id: Target note ID (for append mode)
        new_note_title: Title for new note (for create mode)
        preserve_titles: Add source note titles as headings
        archive_sources: Archive source notes after combination
        separator: Add dividers between notes
    """
    if not source_ids or len(source_ids) < 1:
        output_error("At least one source note ID is required")

    if len(source_ids) > 5:
        output_error("Maximum 5 notes can be combined at once")

    if not target_id and not new_note_title:
        output_error("Either --target-id or --create-new must be provided")

    if target_id and new_note_title:
        output_error("Cannot use both --target-id and --create-new. Choose one.")

    # Read all source notes
    source_notes = []
    for source_id in source_ids:
        note_data = read_note_content(source_id)
        source_notes.append(note_data)
        time.sleep(0.3)  # Rate limiting

    # Build combined blocks
    combined_blocks = []

    for i, note in enumerate(source_notes):
        # Add title as heading if requested
        if preserve_titles:
            combined_blocks.append(create_title_block(note['title']))

        # Add note blocks
        note_blocks = blocks_to_notion_format(note['blocks'])
        combined_blocks.extend(note_blocks)

        # Add separator between notes (but not after last one)
        if separator and i < len(source_notes) - 1:
            combined_blocks.append(create_divider_block())

    if not combined_blocks:
        output_error("No content found in source notes to combine")

    # Execute combination
    result = {}

    if new_note_title:
        # Create new note mode
        new_note = create_new_note(new_note_title, combined_blocks)
        result = {
            "action": "create_combined",
            "target_note": new_note,
            "source_notes": [{"id": n['id'], "title": n['title']} for n in source_notes],
            "blocks_combined": len(combined_blocks)
        }
    else:
        # Append to existing note mode
        blocks_added = append_blocks_to_note(target_id, combined_blocks)

        # Get target note info
        headers = get_headers()
        url = f"{NOTION_BASE_URL}/pages/{target_id}"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            target_title = extract_title(response.json())
        except:
            target_title = "Unknown"

        result = {
            "action": "append_combined",
            "target_note": {
                "id": target_id,
                "name": target_title
            },
            "source_notes": [{"id": n['id'], "title": n['title']} for n in source_notes],
            "blocks_added": blocks_added
        }

    # Archive source notes if requested
    archived_notes = []
    if archive_sources:
        for note in source_notes:
            archive_note(note['id'])
            archived_notes.append(note['id'])
            time.sleep(0.3)  # Rate limiting

    result["archived_sources"] = archived_notes if archive_sources else []

    output_success(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Combine multiple notes into one"
    )
    parser.add_argument("--source-ids", nargs='+', required=True,
                        help="Source note IDs to combine (space-separated, max 5)")
    parser.add_argument("--target-id", help="Target note ID to append to")
    parser.add_argument("--create-new", help="Create new note with this title")
    parser.add_argument("--no-preserve-titles", action="store_true",
                        help="Don't add source note titles as headings")
    parser.add_argument("--no-archive", action="store_true",
                        help="Don't archive source notes after combining")
    parser.add_argument("--no-separator", action="store_true",
                        help="Don't add dividers between notes")

    args = parser.parse_args()

    combine_notes(
        source_ids=args.source_ids,
        target_id=args.target_id,
        new_note_title=args.create_new,
        preserve_titles=not args.no_preserve_titles,
        archive_sources=not args.no_archive,
        separator=not args.no_separator
    )
