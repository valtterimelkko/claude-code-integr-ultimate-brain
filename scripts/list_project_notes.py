#!/usr/bin/env python3
"""
List all notes belonging to a specific project.

This script queries the Notes database and returns all notes for a given project.
"""

import argparse
import requests
import sys
import subprocess
import json
import time
from common import (
    NOTES_DB_ID, NOTION_BASE_URL, get_headers,
    build_project_filter, build_archived_filter, combine_filters,
    output_success, output_error, extract_title
)

def get_project_id_from_name(project_name):
    """
    Find project ID by searching for project name.

    Args:
        project_name: Name of the project to find

    Returns:
        str: Project ID

    Raises:
        SystemExit: If project not found or multiple matches
    """
    import os

    # Try to locate the search_projects.py script
    script_path = "~/.claude/scripts/notion/search_projects.py"
    if not os.path.exists(script_path):
        # Fallback to other possible locations
        fallback_paths = [
            "/root/notion/scripts/skills/search_projects.py",
            os.path.expanduser("~/.claude/scripts/notion/search_projects.py")
        ]
        for path in fallback_paths:
            if os.path.exists(path):
                script_path = path
                break

    try:
        # First try: exact match (case-insensitive)
        result = subprocess.run(
            ["python3", script_path,
             "--name", project_name, "--exact", "--limit", "10"],
            capture_output=True,
            text=True,
            timeout=10
        )

        # If exact match fails, try partial match
        if result.returncode != 0:
            result = subprocess.run(
                ["python3", script_path,
                 "--name", project_name, "--limit", "10"],
                capture_output=True,
                text=True,
                timeout=10
            )

        if result.returncode != 0:
            output_error(f"Project '{project_name}' not found. Try using the search_projects.py script directly to see available projects.")

        data = json.loads(result.stdout)
        if not data['success']:
            output_error(f"Project '{project_name}' not found. Try using the search_projects.py script directly to see available projects.")

        projects = data['data']['projects']
        if len(projects) == 0:
            output_error(f"No projects found matching '{project_name}'. Try using the search_projects.py script directly to see available projects.")
        elif len(projects) > 1:
            project_list = "\n".join([f"  - {p['name']}" for p in projects])
            output_error(
                f"Multiple projects match '{project_name}'. Please be more specific:",
                {"matches": [p['name'] for p in projects]}
            )

        return projects[0]['id'], projects[0]['name']
    except Exception as e:
        output_error(f"Failed to search for project: {str(e)}")

def list_project_notes(project_id=None, project_name=None, include_archived=False, limit=100):
    """
    List all notes for a specific project.

    Args:
        project_id: Project ID (if not provided, project_name is required)
        project_name: Project name to search for
        include_archived: If True, include archived notes
        limit: Maximum results to return
    """
    # Resolve project name to ID if needed
    if project_name and not project_id:
        project_id, resolved_name = get_project_id_from_name(project_name)
        project_name = resolved_name

    if not project_id:
        output_error("Either --project-id or --project-name must be provided")

    headers = get_headers()

    # Build filters
    project_filter = build_project_filter(project_id)
    archived_filter = build_archived_filter(include_archived)
    combined_filter = combine_filters(project_filter, archived_filter)

    # Build request body
    body = {
        "page_size": min(limit, 100)
    }
    if combined_filter:
        body["filter"] = combined_filter

    # Execute query
    url = f"{NOTION_BASE_URL}/databases/{NOTES_DB_ID}/query"
    all_results = []

    try:
        while True:
            response = requests.post(url, headers=headers, json=body, timeout=10)
            response.raise_for_status()

            data = response.json()
            all_results.extend(data.get('results', []))

            # Check if there are more results
            if not data.get('has_more', False):
                break

            # Set up pagination
            body['start_cursor'] = data.get('next_cursor')
            time.sleep(0.3)  # Rate limiting
    except requests.exceptions.RequestException as e:
        output_error(f"API request failed: {str(e)}")

    # Limit results
    all_results = all_results[:limit]

    # Format results
    notes = []
    for note in all_results:
        notes.append({
            "id": note['id'],
            "name": extract_title(note),
            "created": note.get('created_time'),
            "updated": note.get('last_edited_time'),
            "archived": note.get('archived', False)
        })

    output_success({
        "project": {
            "id": project_id,
            "name": project_name or "Unknown"
        },
        "include_archived": include_archived,
        "count": len(notes),
        "notes": notes
    })

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="List all notes for a specific project"
    )
    parser.add_argument("--project-id", help="Project ID")
    parser.add_argument("--project-name", help="Project name to search for")
    parser.add_argument("--include-archived", action="store_true", help="Include archived notes")
    parser.add_argument("--limit", type=int, default=100, help="Maximum results")

    args = parser.parse_args()

    if not args.project_id and not args.project_name:
        output_error("Either --project-id or --project-name must be provided")

    list_project_notes(
        project_id=args.project_id,
        project_name=args.project_name,
        include_archived=args.include_archived,
        limit=args.limit
    )
