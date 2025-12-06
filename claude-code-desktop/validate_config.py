#!/usr/bin/env python3
"""
Validate Ultimate Brain Claude Code configuration.

This script checks that:
1. Database IDs are configured (not still placeholders)
2. Python scripts are installed
3. Skill definitions are in place
4. Notion token is accessible
5. Can connect to Notion API

Usage:
    python3 validate_config.py
"""

import sys
import os
import json
import subprocess
from pathlib import Path


class ConfigValidator:
    """Validates Ultimate Brain configuration."""

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.checks = []
        self.claude_dir = Path.home() / ".claude"
        self.scripts_dir = self.claude_dir / "scripts" / "notion"
        self.skills_dir = self.claude_dir / "skills"
        self.token_file = Path("/etc/keep-to-notion/env.conf")

    def check(self, name, func):
        """Run a check and track results."""
        try:
            result = func()
            self.checks.append((name, result))
            return result
        except Exception as e:
            self.errors.append(f"{name}: {str(e)}")
            return False

    # ========================================================================
    # CHECKS
    # ========================================================================

    def check_common_py(self):
        """Check if common.py exists and has database IDs."""
        common_py = self.scripts_dir / "common.py"

        if not common_py.exists():
            self.errors.append("Python scripts not found at ~/.claude/scripts/notion/")
            return False

        with open(common_py) as f:
            content = f.read()

        if "YOUR_NOTES_DATABASE_ID_HERE" in content:
            self.errors.append(
                "Database IDs not configured in scripts/common.py\n"
                "    Please edit: ~/.claude/scripts/notion/common.py\n"
                "    Replace: YOUR_NOTES_DATABASE_ID_HERE → your actual ID\n"
                "    Replace: YOUR_PROJECTS_DATABASE_ID_HERE → your actual ID\n"
                "    Or run: ./install.sh to configure automatically"
            )
            return False

        if "YOUR_PROJECTS_DATABASE_ID_HERE" in content:
            self.errors.append(
                "Projects database ID not configured in scripts/common.py\n"
                "    Please edit: ~/.claude/scripts/notion/common.py\n"
                "    Replace: YOUR_PROJECTS_DATABASE_ID_HERE → your actual ID"
            )
            return False

        return True

    def check_scripts_installed(self):
        """Check if all required scripts are installed."""
        required_scripts = [
            "common.py",
            "search_notes.py",
            "read_note.py",
            "list_project_notes.py",
            "create_note.py",
            "edit_note.py",
            "search_projects.py",
        ]

        missing = []
        for script in required_scripts:
            script_path = self.scripts_dir / script
            if not script_path.exists():
                missing.append(script)

        if missing:
            self.errors.append(
                f"Missing Python scripts: {', '.join(missing)}\n"
                "    Run: ./install.sh to install all scripts"
            )
            return False

        return True

    def check_skills_installed(self):
        """Check if all Claude Code skills are installed."""
        required_skills = [
            "notion-search-notes",
            "notion-read-note",
            "notion-list-project-notes",
            "notion-create-note",
            "notion-edit-note",
        ]

        missing = []
        for skill in required_skills:
            skill_path = self.skills_dir / skill / "SKILL.md"
            if not skill_path.exists():
                missing.append(skill)

        if missing:
            self.warnings.append(
                f"Missing skill definitions: {', '.join(missing)}\n"
                "    They should be at: ~/.claude/skills/notion-{skill-name}/SKILL.md\n"
                "    Run: ./install.sh to install all skills"
            )
            return False

        return True

    def check_token_file(self):
        """Check if Notion token file exists and is readable."""
        if not self.token_file.exists():
            self.errors.append(
                f"Notion token file not found: {self.token_file}\n"
                "    Create it with: echo 'NOTION_TOKEN=secret_...' | sudo tee {self.token_file}\n"
                "    Or run: ./install.sh to create it automatically"
            )
            return False

        # Check if readable
        try:
            with open(self.token_file) as f:
                content = f.read()
            if "NOTION_TOKEN=" not in content:
                self.errors.append(f"NOTION_TOKEN not found in {self.token_file}")
                return False
        except PermissionError:
            self.errors.append(f"Cannot read {self.token_file} (permission denied)")
            return False

        return True

    def check_python_imports(self):
        """Check if required Python libraries are available."""
        required_modules = ["requests", "json", "sys"]

        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                self.warnings.append(f"Missing Python module: {module}")
                return False

        return True

    def check_api_connectivity(self):
        """Try to connect to Notion API."""
        try:
            # Try to run search_projects with a test query
            result = subprocess.run(
                [
                    sys.executable,
                    str(self.scripts_dir / "search_projects.py"),
                    "--name",
                    "test",
                    "--limit",
                    "1",
                ],
                capture_output=True,
                timeout=5,
                text=True,
            )

            if result.returncode == 0:
                # Try to parse output as JSON
                try:
                    output = json.loads(result.stdout)
                    if output.get("success"):
                        return True
                except json.JSONDecodeError:
                    pass

            # If we get here, the API call didn't work
            stderr = result.stderr or result.stdout
            if "NOTION_TOKEN" in stderr or "permission" in stderr.lower():
                self.errors.append(
                    "Cannot connect to Notion API - token may be invalid or expired\n"
                    "    Update your token at: /etc/keep-to-notion/env.conf\n"
                    "    Get a new token: https://www.notion.so/my-integrations"
                )
            else:
                self.warnings.append(
                    "Could not verify API connectivity\n"
                    "    This is OK if your token or database IDs are incomplete\n"
                    f"    Error: {stderr[:200]}"
                )
            return False

        except subprocess.TimeoutExpired:
            self.warnings.append("API connectivity check timed out")
            return False
        except Exception as e:
            self.warnings.append(f"Could not test API connectivity: {str(e)}")
            return False

    # ========================================================================
    # VALIDATION
    # ========================================================================

    def validate(self):
        """Run all validation checks."""
        print("🔍 Validating Ultimate Brain Configuration\n")
        print("=" * 60)

        self.check("Database IDs Configured", self.check_common_py)
        self.check("Scripts Installed", self.check_scripts_installed)
        self.check("Skills Installed", self.check_skills_installed)
        self.check("Token File Present", self.check_token_file)
        self.check("Python Imports", self.check_python_imports)
        self.check("API Connectivity", self.check_api_connectivity)

        self.print_results()
        return len(self.errors) == 0

    def print_results(self):
        """Print validation results."""
        print("\nValidation Results:\n")

        for name, result in self.checks:
            status = "✅" if result else "❌"
            print(f"{status} {name}")

        if self.warnings:
            print("\n" + "=" * 60)
            print("⚠️  Warnings:\n")
            for warning in self.warnings:
                print(f"  • {warning}\n")

        if self.errors:
            print("=" * 60)
            print("❌ Errors:\n")
            for error in self.errors:
                print(f"  • {error}\n")

        print("=" * 60)

        if not self.errors:
            print(
                "\n✅ Configuration is valid! You're ready to use Claude Code.\n"
                "\n📚 Next steps:"
                "\n  1. Restart Claude Code (VS Code) or Claude Desktop"
                "\n  2. Your 5 skills should be available:"
                "\n     - notion_search_notes"
                "\n     - notion_read_note"
                "\n     - notion_list_project_notes"
                "\n     - notion_create_note"
                "\n     - notion_edit_note"
                "\n  3. Try asking: 'Search my notes for test'"
                "\n"
            )
        else:
            print("\n❌ Configuration has errors - please fix them above.\n")
            print("📚 For help:")
            print("  • See: ./README.md")
            print("  • Check: ../README.md")
            print("  • Run: ./install.sh\n")


def main():
    """Run the validator."""
    validator = ConfigValidator()
    is_valid = validator.validate()
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
