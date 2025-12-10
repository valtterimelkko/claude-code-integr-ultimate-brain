#!/usr/bin/env python3
"""
Archive or unarchive a Notion note.

This script toggles the Archived property (checkbox) for a note in the
Ultimate Brain system.
"""

import argparse
import requests
import sys
import subprocess
import json
from common import (
    NOTES_DB_ID, NOTION_BASE_URL, get_headers,
    build_title_filter, build_project_filter, build_archived_filter, combine_filters,
    output_success, output_error, extract_title
)

def find_note_by_name(note_name, project_name=None, include_archived=False):
    """
    Find a note by name (and optionally by project).

    Args:
        note_name: Name of the note to find
        project_name: Optional project name to limit search
        include_archived: Whether to include archived notes in search

    Returns:
        tuple: (note_id, current_archived_status)
    """
    headers = get_headers()
    title_filter = build_title_filter(note_name)

    # If project name provided, resolve it first
    project_id = None
    if project_name:
        import os
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
    archived_filter = build_archived_filter(include_archived=include_archived)
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
        page = exact_matches[0]
        archived_status = page.get('properties', {}).get('Archived', {}).get('checkbox', False)
        return page['id'], archived_status

    # If multiple matches, ask for clarification
    if len(results) > 1:
        matches = [extract_title(r) for r in results[:5]]
        output_error(
            f"Multiple notes match '{note_name}'. Please be more specific:",
            {"matches": matches}
        )

    page = results[0]
    archived_status = page.get('properties', {}).get('Archived', {}).get('checkbox', False)
    return page['id'], archived_status

def get_note_archived_status(note_id):
    """
    Get the current archived status of a note.

    Args:
        note_id: Note ID

    Returns:
        bool: Current archived status
    """
    headers = get_headers()
    url = f"{NOTION_BASE_URL}/pages/{note_id}"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        output_error(f"Failed to fetch note: {str(e)}")

    page = response.json()
    return page.get('properties', {}).get('Archived', {}).get('checkbox', False)

def archive_note(note_id=None, note_name=None, project_name=None, action="archive"):
    """
    Archive or unarchive a note.

    Args:
        note_id: Note ID (if not provided, note_name is required)
        note_name: Note name to search for
        project_name: Optional project name to limit search
        action: "archive" or "unarchive"
    """
    # Resolve note name to ID if needed
    current_archived_status = None
    if note_name and not note_id:
        # Include archived notes in search if we're trying to unarchive
        include_archived = (action == "unarchive")
        note_id, current_archived_status = find_note_by_name(note_name, project_name, include_archived)

    if not note_id:
        output_error("Either --id or --name must be provided")

    # Get current status and note metadata
    headers = get_headers()
    url = f"{NOTION_BASE_URL}/pages/{note_id}"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        output_error(f"Failed to fetch note: {str(e)}")

    page = response.json()
    note_title = extract_title(page)

    if current_archived_status is None:
        current_archived_status = page.get('properties', {}).get('Archived', {}).get('checkbox', False)

    # Determine new status
    if action == "archive":
        new_status = True
    elif action == "unarchive":
        new_status = False
    else:
        output_error(f"Unknown action: {action}")

    # Check if already in desired state
    if current_archived_status == new_status:
        output_success({
            "action": action,
            "note": {
                "id": note_id,
                "name": note_title
            },
            "status": "no_change",
            "message": f"Note is already {'archived' if new_status else 'not archived'}"
        })

    # Update the archived property
    update_data = {
        "properties": {
            "Archived": {
                "checkbox": new_status
            }
        }
    }

    try:
        response = requests.patch(url, headers=headers, json=update_data, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        output_error(f"Failed to update note: {str(e)}")

    output_success({
        "action": action,
        "note": {
            "id": note_id,
            "name": note_title
        },
        "status": "updated",
        "archived": new_status,
        "message": f"Note successfully {'archived' if new_status else 'unarchived'}"
    })

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Archive or unarchive a note in the Ultimate Brain system"
    )
    parser.add_argument("--id", help="Note ID to archive/unarchive")
    parser.add_argument("--name", help="Note name to search for")
    parser.add_argument("--project-name", help="Optional project name for name search")
    parser.add_argument("--action", choices=["archive", "unarchive"], default="archive",
                        help="Action to perform (default: archive)")

    args = parser.parse_args()

    if not args.id and not args.name:
        output_error("Either --id or --name must be provided")

    archive_note(
        note_id=args.id,
        note_name=args.name,
        project_name=args.project_name,
        action=args.action
    )
