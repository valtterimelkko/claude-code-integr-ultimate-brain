#!/usr/bin/env python3
"""
Search for projects by name in the Notion Projects database.

This script searches the Projects database and returns matching project records.
"""

import argparse
import requests
import sys
import time
from common import (
    PROJECTS_DB_ID, NOTION_BASE_URL, get_headers,
    build_title_filter, build_archived_filter, combine_filters,
    output_success, output_error, extract_title
)

def extract_status(page):
    """Extract status from a project page."""
    status_prop = page.get('properties', {}).get('Status', {})
    if status_prop.get('type') == 'status':
        status_obj = status_prop.get('status', {})
        return status_obj.get('name', 'Unknown')
    return None

def search_projects(name, exact_match=False, include_archived=False, limit=10):
    """
    Search for projects by name.

    Args:
        name: Project name to search for
        exact_match: If True, require exact match
        include_archived: If True, include archived projects
        limit: Maximum results to return

    Returns:
        dict: Search results with project list
    """
    headers = get_headers()

    # Build filters
    title_filter = build_title_filter(name)
    archived_filter = build_archived_filter(include_archived)
    combined_filter = combine_filters(title_filter, archived_filter)

    # Build request body
    body = {
        "page_size": min(limit, 100)
    }
    if combined_filter:
        body["filter"] = combined_filter

    # Execute query
    url = f"{NOTION_BASE_URL}/databases/{PROJECTS_DB_ID}/query"

    try:
        response = requests.post(url, headers=headers, json=body, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        output_error(f"API request failed: {str(e)}")

    data = response.json()
    results = data.get('results', [])

    # If exact match requested, filter results
    if exact_match:
        results = [r for r in results if extract_title(r).lower() == name.lower()]

    # Limit results
    results = results[:limit]

    # If no results found
    if not results:
        output_error(
            f"No projects found matching '{name}'",
            {"query": name, "exact_match": exact_match}
        )

    # Format results
    projects = []
    for project in results:
        projects.append({
            "id": project['id'],
            "name": extract_title(project),
            "status": extract_status(project),
            "archived": project.get('archived', False)
        })

    output_success({
        "query": name,
        "exact_match": exact_match,
        "include_archived": include_archived,
        "count": len(projects),
        "projects": projects
    })

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Search for projects by name in Notion"
    )
    parser.add_argument("--name", required=True, help="Project name to search for")
    parser.add_argument("--exact", action="store_true", help="Require exact match")
    parser.add_argument("--include-archived", action="store_true", help="Include archived projects")
    parser.add_argument("--limit", type=int, default=10, help="Maximum results")

    args = parser.parse_args()

    search_projects(
        name=args.name,
        exact_match=args.exact,
        include_archived=args.include_archived,
        limit=args.limit
    )
