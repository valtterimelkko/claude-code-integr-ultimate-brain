#!/usr/bin/env python3
"""
Search for notes by keyword in the Notion Notes database.

This script searches the Notes database by title and optionally filters by project.
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
    output_success, output_error, extract_title
)

def get_project_id_from_name(project_name):
    """
    Find project ID by searching for project name.

    Args:
        project_name: Name of the project to find

    Returns:
        tuple: (project_id, project_name)

    Raises:
        SystemExit: If project not found or multiple matches
    """
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
             "--name", project_name, "--limit", "10"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            output_error(f"Project '{project_name}' not found")

        data = json.loads(result.stdout)
        if not data['success']:
            output_error(f"Project '{project_name}' not found")

        projects = data['data']['projects']
        if len(projects) == 0:
            output_error(f"No projects found matching '{project_name}'")
        elif len(projects) > 1:
            project_list = "\n".join([f"  - {p['name']}" for p in projects])
            output_error(
                f"Multiple projects match '{project_name}'. Please be more specific:",
                {"matches": [p['name'] for p in projects]}
            )

        return projects[0]['id'], projects[0]['name']
    except Exception as e:
        output_error(f"Failed to search for project: {str(e)}")

def get_project_name_from_id(project_id):
    """
    Get project name from ID by fetching the page.

    Args:
        project_id: Project page ID

    Returns:
        str: Project name or None if not found
    """
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

def search_notes(query, project_id=None, project_name=None, include_archived=False, limit=20):
    """
    Search for notes by keyword.

    Args:
        query: Search term for note titles
        project_id: Optional project ID to limit search
        project_name: Optional project name to limit search
        include_archived: If True, include archived notes
        limit: Maximum results to return
    """
    # Resolve project name to ID if needed
    if project_name and not project_id:
        project_id, project_name = get_project_id_from_name(project_name)
    elif project_id and not project_name:
        # Try to get name from ID
        project_name = get_project_name_from_id(project_id)

    headers = get_headers()

    # Build filters
    title_filter = build_title_filter(query)
    archived_filter = build_archived_filter(include_archived)
    project_filter = build_project_filter(project_id) if project_id else None
    combined_filter = combine_filters(title_filter, archived_filter, project_filter)

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

    # If no results found
    if not all_results:
        output_success({
            "query": query,
            "project": project_name if project_id else None,
            "include_archived": include_archived,
            "count": 0,
            "notes": []
        })

    # Format results
    notes = []
    for note in all_results:
        # Try to get project relation
        note_project = None
        project_prop = note.get('properties', {}).get('Project', {})
        if project_prop.get('type') == 'relation':
            relations = project_prop.get('relation', [])
            if relations:
                note_project_id = relations[0].get('id')
                note_project = get_project_name_from_id(note_project_id)

        notes.append({
            "id": note['id'],
            "name": extract_title(note),
            "project_name": note_project,
            "created": note.get('created_time'),
            "archived": note.get('archived', False)
        })

    output_success({
        "query": query,
        "project": project_name if project_id else None,
        "include_archived": include_archived,
        "count": len(notes),
        "notes": notes
    })

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Search for notes by keyword"
    )
    parser.add_argument("--query", required=True, help="Search term for note titles")
    parser.add_argument("--project-id", help="Optional project ID to limit search")
    parser.add_argument("--project-name", help="Optional project name to limit search")
    parser.add_argument("--include-archived", action="store_true", help="Include archived notes")
    parser.add_argument("--limit", type=int, default=20, help="Maximum results")

    args = parser.parse_args()

    search_notes(
        query=args.query,
        project_id=args.project_id,
        project_name=args.project_name,
        include_archived=args.include_archived,
        limit=args.limit
    )
