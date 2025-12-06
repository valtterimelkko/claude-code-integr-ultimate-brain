#!/usr/bin/env python3
"""
Common utilities for Notion skill scripts.

This module provides:
- Credential loading
- API headers configuration
- Database ID constants
- Text extraction helpers
- JSON output formatting
- Error response formatting
"""

import json
import sys

# ============================================================================
# CONSTANTS
# ============================================================================

# Database IDs (formatted with dashes for API calls)
# REPLACE THESE WITH YOUR ACTUAL DATABASE IDs FROM YOUR ULTIMATE BRAIN SETUP
NOTES_DB_ID = "YOUR_NOTES_DATABASE_ID_HERE"
PROJECTS_DB_ID = "YOUR_PROJECTS_DATABASE_ID_HERE"

# API configuration
NOTION_API_VERSION = "2022-06-28"
NOTION_BASE_URL = "https://api.notion.com/v1"

# ============================================================================
# CREDENTIAL LOADING
# ============================================================================

def load_credentials():
    """
    Load Notion API token from config file.

    Returns:
        str: The Notion API token

    Raises:
        SystemExit: If token cannot be loaded
    """
    try:
        with open('/etc/keep-to-notion/env.conf') as f:
            for line in f:
                if line.startswith('NOTION_TOKEN='):
                    return line.split('=', 1)[1].strip()
        output_error("NOTION_TOKEN not found in config file")
        sys.exit(1)
    except FileNotFoundError:
        output_error("Config file not found: /etc/keep-to-notion/env.conf")
        sys.exit(1)

def get_headers():
    """
    Get standard Notion API headers.

    Returns:
        dict: Headers dict with Authorization, Notion-Version, Content-Type
    """
    token = load_credentials()
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_API_VERSION,
        "Content-Type": "application/json"
    }

# ============================================================================
# TEXT EXTRACTION
# ============================================================================

def extract_title(page):
    """
    Extract title from a Notion page object.

    Args:
        page: Notion page object from API response

    Returns:
        str: The page title, or "Untitled" if not found
    """
    title_prop = page.get('properties', {}).get('Name', {})
    if title_prop.get('type') == 'title':
        title_array = title_prop.get('title', [])
        if title_array:
            return title_array[0].get('plain_text', 'Untitled')
    return "Untitled"

def extract_block_text(block):
    """
    Extract plain text from a Notion block.

    Args:
        block: Notion block object from API response

    Returns:
        dict: {"type": block_type, "text": extracted_text}
    """
    block_type = block.get('type', 'unknown')

    # Block types that contain rich_text
    rich_text_types = [
        'paragraph', 'heading_1', 'heading_2', 'heading_3',
        'bulleted_list_item', 'numbered_list_item', 'to_do',
        'toggle', 'quote', 'callout'
    ]

    if block_type in rich_text_types:
        rich_text = block.get(block_type, {}).get('rich_text', [])
        text = ''.join([rt.get('plain_text', '') for rt in rich_text])
        return {"type": block_type, "text": text}

    elif block_type == 'code':
        rich_text = block.get('code', {}).get('rich_text', [])
        text = ''.join([rt.get('plain_text', '') for rt in rich_text])
        language = block.get('code', {}).get('language', 'plain text')
        return {"type": "code", "language": language, "text": text}

    elif block_type == 'divider':
        return {"type": "divider", "text": "---"}

    elif block_type == 'image':
        url = block.get('image', {}).get('file', {}).get('url', '')
        if not url:
            url = block.get('image', {}).get('external', {}).get('url', '')
        return {"type": "image", "text": f"[Image: {url}]"}

    else:
        return {"type": block_type, "text": f"[{block_type} block]"}

# ============================================================================
# OUTPUT FORMATTING
# ============================================================================

def output_success(data):
    """
    Output successful JSON response and exit.

    Args:
        data: Dictionary to output as JSON
    """
    result = {"success": True, "data": data}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0)

def output_error(message, details=None):
    """
    Output error JSON response and exit.

    Args:
        message: Error message string
        details: Optional additional details
    """
    result = {"success": False, "error": message}
    if details:
        result["details"] = details
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(1)

# ============================================================================
# FILTER BUILDERS
# ============================================================================

def build_archived_filter(include_archived=False):
    """
    Build filter to exclude/include archived items.

    Args:
        include_archived: If True, don't filter archived items

    Returns:
        dict: Filter object, or None if include_archived is True
    """
    if include_archived:
        return None
    return {
        "property": "Archived",
        "checkbox": {"equals": False}
    }

def build_project_filter(project_id):
    """
    Build filter for project relation.

    Args:
        project_id: Project page ID

    Returns:
        dict: Filter object
    """
    return {
        "property": "Project",
        "relation": {"contains": project_id}
    }

def build_title_filter(search_term):
    """
    Build filter for title search.

    Args:
        search_term: Text to search for in title

    Returns:
        dict: Filter object
    """
    return {
        "property": "Name",
        "title": {"contains": search_term}
    }

def combine_filters(*filters):
    """
    Combine multiple filters with AND logic.

    Args:
        *filters: Filter objects (None values are ignored)

    Returns:
        dict: Combined filter object
    """
    valid_filters = [f for f in filters if f is not None]

    if len(valid_filters) == 0:
        return None
    elif len(valid_filters) == 1:
        return valid_filters[0]
    else:
        return {"and": valid_filters}
