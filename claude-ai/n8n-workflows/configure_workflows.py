#!/usr/bin/env python3
"""
Configure n8n workflow files with your database IDs.

Usage:
    python3 configure_workflows.py \\
        --notes-db "YOUR_NOTES_DATABASE_ID" \\
        --projects-db "YOUR_PROJECTS_DATABASE_ID" \\
        --output-dir ./configured

This script reads each workflow-*.json file, replaces placeholder database IDs
with your actual values, and writes configured versions to the output directory.
"""

import json
import argparse
import os
from pathlib import Path
import sys


def validate_database_id(db_id, name):
    """Validate that a database ID looks correct."""
    if not db_id or len(db_id) < 10:
        print(f"❌ Error: {name} is too short. Expected format: 2bf45010-ad5d-816a-8e25-f1f4d80a12a7")
        return False
    if " " in db_id:
        print(f"❌ Error: {name} contains spaces. Remove any extra whitespace.")
        return False
    return True


def configure_workflow(input_file, notes_db, projects_db, output_dir, verbose=False):
    """
    Configure a single workflow file.

    Args:
        input_file: Path to workflow JSON file
        notes_db: Notes database ID
        projects_db: Projects database ID
        output_dir: Directory to write configured file
        verbose: Print detailed output

    Returns:
        dict with configuration result
    """
    try:
        # Read the JSON file
        with open(input_file, 'r') as f:
            content = f.read()
            workflow = json.loads(content)
    except json.JSONDecodeError as e:
        return {
            "file": input_file,
            "success": False,
            "error": f"Invalid JSON: {str(e)}"
        }
    except FileNotFoundError:
        return {
            "file": input_file,
            "success": False,
            "error": f"File not found: {input_file}"
        }

    # Track what was replaced
    replacements = {
        "notes_db": 0,
        "projects_db": 0,
        "paths": 0
    }

    # Convert to string for replacement (preserving formatting)
    workflow_str = json.dumps(workflow, indent=2)

    original_str = workflow_str

    # Replace database ID placeholders
    if "YOUR_NOTES_DATABASE_ID_HERE" in workflow_str:
        workflow_str = workflow_str.replace("YOUR_NOTES_DATABASE_ID_HERE", notes_db)
        replacements["notes_db"] = workflow_str.count(notes_db)

    if "YOUR_PROJECTS_DATABASE_ID_HERE" in workflow_str:
        workflow_str = workflow_str.replace("YOUR_PROJECTS_DATABASE_ID_HERE", projects_db)
        replacements["projects_db"] = workflow_str.count(projects_db)

    # Parse back to JSON
    try:
        workflow = json.loads(workflow_str)
    except json.JSONDecodeError as e:
        return {
            "file": input_file,
            "success": False,
            "error": f"JSON error after replacement: {str(e)}"
        }

    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Write the configured file
    output_file = output_path / Path(input_file).name
    try:
        with open(output_file, 'w') as f:
            json.dump(workflow, f, indent=2)

        if verbose:
            print(f"  ✓ {Path(input_file).name}")
            if replacements["notes_db"] > 0:
                print(f"    - Notes DB replaced in {replacements['notes_db']} locations")
            if replacements["projects_db"] > 0:
                print(f"    - Projects DB replaced in {replacements['projects_db']} locations")

        return {
            "file": input_file,
            "success": True,
            "output": str(output_file),
            "replacements": replacements
        }
    except Exception as e:
        return {
            "file": input_file,
            "success": False,
            "error": f"Failed to write output: {str(e)}"
        }


def main():
    parser = argparse.ArgumentParser(
        description="Configure n8n workflow files with your database IDs"
    )
    parser.add_argument(
        "--notes-db",
        required=True,
        help="Your Notion Notes database ID"
    )
    parser.add_argument(
        "--projects-db",
        required=True,
        help="Your Notion Projects database ID"
    )
    parser.add_argument(
        "--output-dir",
        default="./configured",
        help="Output directory for configured files (default: ./configured)"
    )
    parser.add_argument(
        "--input-dir",
        default=".",
        help="Directory containing workflow JSON files (default: current directory)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed output"
    )

    args = parser.parse_args()

    # Validate database IDs
    print("🔍 Validating database IDs...\n")

    if not validate_database_id(args.notes_db, "Notes DB ID"):
        return 1
    if not validate_database_id(args.projects_db, "Projects DB ID"):
        return 1

    print(f"✅ Notes DB ID: {args.notes_db[:12]}...")
    print(f"✅ Projects DB ID: {args.projects_db[:12]}...\n")

    # Find all workflow files
    input_dir = Path(args.input_dir)
    workflow_files = sorted(input_dir.glob("workflow-*.json"))

    if not workflow_files:
        print(f"❌ Error: No workflow-*.json files found in {args.input_dir}")
        return 1

    print(f"📋 Found {len(workflow_files)} workflow files\n")

    # Configure each workflow
    print("⚙️  Configuring workflows...\n")
    results = []

    for workflow_file in workflow_files:
        result = configure_workflow(
            str(workflow_file),
            args.notes_db,
            args.projects_db,
            args.output_dir,
            verbose=args.verbose
        )
        results.append(result)

    # Summary
    successful = sum(1 for r in results if r["success"])
    failed = sum(1 for r in results if not r["success"])

    print(f"\n{'='*60}")

    if failed == 0:
        print(f"✅ Configured {successful} workflows successfully!\n")
        print(f"📁 Configured files are in: {Path(args.output_dir).absolute()}/\n")
        print("📤 Next steps:")
        print("  1. Go to n8n → Workflows → Import")
        print(f"  2. Select all files from: {Path(args.output_dir).absolute()}/")
        print("  3. Click Import")
        print("  4. Test each workflow before activating\n")
        return 0
    else:
        print(f"⚠️  Configured {successful} workflows, {failed} failed\n")
        for result in results:
            if not result["success"]:
                print(f"❌ {result['file']}: {result['error']}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
