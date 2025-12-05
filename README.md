# Notion Claude Code Skills for Ultimate Brain

A collection of Claude Code skills that enable efficient interaction with your **Thomas Frank's Ultimate Brain** Notion workspace. These skills provide structured, reliable access to your Notion Notes and Projects databases through simple, context-efficient operations.

## 📋 Table of Contents

- [Overview](#overview)
- [Available Skills](#available-skills)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Step 1: Set Up Notion Integration](#step-1-set-up-notion-integration)
  - [Step 2: Find Your Database IDs](#step-2-find-your-database-ids)
  - [Step 3: Configure the Scripts](#step-3-configure-the-scripts)
  - [Step 4: Set Up Environment File](#step-4-set-up-environment-file)
  - [Step 5: Install the Skills](#step-5-install-the-skills)
  - [Step 6: Test the Installation](#step-6-test-the-installation)
- [Usage](#usage)
- [Architecture](#architecture)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This skills system is **optimized for Thomas Frank's Ultimate Brain system on Notion**. It currently supports working with **Notes** in your Ultimate Brain workspace, with a focus on reliability, context efficiency, and respecting Notion API rate limits.

### Key Features

- **Structured Output**: All operations return JSON with guaranteed format
- **Archived Filtering**: Automatically excludes archived notes unless explicitly requested
- **Name Resolution**: Search for projects and notes by partial name match
- **Error Handling**: Clear, actionable error messages
- **Context Efficient**: Returns only needed data, doesn't overload your context window
- **Rate Limit Compliant**: Built-in delays (0.3s between API calls) to respect Notion's limits

## 🛠️ Available Skills

Five skills are available for use in Claude Code:

1. **`notion-create-note`** - Create a new note in the Note inbox
2. **`notion-list-project-notes`** - List all notes in a specific project
3. **`notion-search-notes`** - Search for notes by keyword
4. **`notion-read-note`** - Read the full content of a note
5. **`notion-edit-note`** - Edit note content (append, replace, or clear)

Each skill has comprehensive documentation in the [`skill-definitions/`](skill-definitions/) folder.

## ✅ Prerequisites

Before you begin, ensure you have:

- **Thomas Frank's Ultimate Brain** Notion workspace set up
- **Notion account** (free tier is sufficient - the Notion API is generous for personal use)
- **Python 3.7+** installed on your system
- **`requests`** library for Python (`pip install requests`)
- **Claude Code** installed and configured
- Basic familiarity with command line operations

## 📦 Installation

### Step 1: Set Up Notion Integration

1. **Go to Notion Integrations page**: Visit [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)

2. **Create a new integration**:
   - Click **"+ New integration"**
   - Give it a name (e.g., "Claude Code Skills")
   - Select the workspace where your Ultimate Brain is located
   - Click **"Submit"**

3. **Copy the Integration Token**:
   - After creating, you'll see an **"Internal Integration Token"**
   - Click **"Show"** then **"Copy"** to copy the token
   - **IMPORTANT**: Keep this token secure! It provides access to your Notion workspace
   - The token will look like: `secret_ABC123xyz...`

4. **Share your databases with the integration**:
   - Open your **Ultimate Brain** workspace in Notion
   - Navigate to the **"Databases & Components"** page
   - Open your **Notes** database (full page view)
   - Click the **"..."** menu in the top right
   - Scroll down and click **"+ Add connections"**
   - Search for and select your integration (e.g., "Claude Code Skills")
   - Repeat for the **Projects** database

### Step 2: Find Your Database IDs

You'll need the IDs for two databases: **Notes** and **Projects**.

#### Finding Database IDs:

1. **Navigate to Databases & Components**:
   - In your Ultimate Brain workspace, find the link to **"Databases & Components"**
   - This is typically on your dashboard/home page

2. **Open the Notes database**:
   - Click on the **Notes** database to open it in full page view
   - Look at the URL in your browser's address bar
   - The URL will look like: `https://www.notion.so/a1b2c3d4e5f67890a1b2c3d4e5f67890?v=...`
   - The database ID is the long string of letters and numbers: `a1b2c3d4e5f67890a1b2c3d4e5f67890`
   - **Copy this ID** - you'll need it in Step 3

3. **Open the Projects database**:
   - Go back to "Databases & Components"
   - Click on the **Projects** database
   - Look at the URL again
   - The URL will look like: `https://www.notion.so/1234567890abcdef1234567890abcdef?v=...`
   - The database ID is: `1234567890abcdef1234567890abcdef`
   - **Copy this ID** - you'll need it in Step 3

**Important Notes**:
- Database IDs are **32 characters long** (letters and numbers, no dashes in the URL)
- Don't include the `?v=` part or anything after it
- Don't worry about dashes - the script will format them correctly

### Step 3: Configure the Scripts

1. **Clone or download this repository** to your local machine:
   ```bash
   git clone https://github.com/YOUR_USERNAME/notion-claude-code-skills.git
   cd notion-claude-code-skills
   ```

2. **Edit the `scripts/common.py` file**:
   ```bash
   nano scripts/common.py
   # or use your preferred text editor
   ```

3. **Replace the placeholder database IDs** on lines 22-23:

   **BEFORE** (what you'll see):
   ```python
   # Database IDs (formatted with dashes for API calls)
   # REPLACE THESE WITH YOUR ACTUAL DATABASE IDs FROM YOUR ULTIMATE BRAIN SETUP
   NOTES_DB_ID = "YOUR_NOTES_DATABASE_ID_HERE"
   PROJECTS_DB_ID = "YOUR_PROJECTS_DATABASE_ID_HERE"
   ```

   **AFTER** (example with your IDs - with dashes added):
   ```python
   # Database IDs (formatted with dashes for API calls)
   NOTES_DB_ID = "a1b2c3d4-e5f6-7890-a1b2-c3d4e5f67890"
   PROJECTS_DB_ID = "12345678-90ab-cdef-1234-567890abcdef"
   ```

   **⚠️ IMPORTANT**: Format your database IDs with dashes in this pattern: `8-4-4-4-12` characters
   - Example: If your ID from the URL is `a1b2c3d4e5f67890a1b2c3d4e5f67890`
   - Format it as: `a1b2c3d4-e5f6-7890-a1b2-c3d4e5f67890`

4. **Save the file** and exit the editor

### Step 4: Set Up Environment File

The scripts need to access your Notion Integration Token. We'll store it securely in a configuration file.

1. **Create the configuration directory**:
   ```bash
   sudo mkdir -p /etc/keep-to-notion
   ```

2. **Create the configuration file**:
   ```bash
   sudo nano /etc/keep-to-notion/env.conf
   ```

3. **Add your Notion token**:
   ```
   NOTION_TOKEN=secret_YOUR_TOKEN_FROM_STEP_1_HERE
   ```

   Replace `secret_YOUR_TOKEN_FROM_STEP_1_HERE` with the actual integration token you copied in Step 1.

4. **Save and secure the file**:
   ```bash
   sudo chmod 600 /etc/keep-to-notion/env.conf
   ```

   This ensures only root can read the file containing your token.

### Step 5: Install the Skills

1. **Copy the scripts to Claude's scripts directory**:
   ```bash
   mkdir -p ~/.claude/scripts/notion
   cp scripts/*.py ~/.claude/scripts/notion/
   chmod +x ~/.claude/scripts/notion/*.py
   ```

2. **Copy the skill definitions to Claude's skills directory**:
   ```bash
   mkdir -p ~/.claude/skills

   # Copy each skill
   cp -r skill-definitions/notion-create-note.md ~/.claude/skills/notion-create-note/SKILL.md
   cp -r skill-definitions/notion-edit-note.md ~/.claude/skills/notion-edit-note/SKILL.md
   cp -r skill-definitions/notion-list-project-notes.md ~/.claude/skills/notion-list-project-notes/SKILL.md
   cp -r skill-definitions/notion-read-note.md ~/.claude/skills/notion-read-note/SKILL.md
   cp -r skill-definitions/notion-search-notes.md ~/.claude/skills/notion-search-notes/SKILL.md
   ```

   Or create the directory structure first:
   ```bash
   mkdir -p ~/.claude/skills/notion-create-note
   mkdir -p ~/.claude/skills/notion-edit-note
   mkdir -p ~/.claude/skills/notion-list-project-notes
   mkdir -p ~/.claude/skills/notion-read-note
   mkdir -p ~/.claude/skills/notion-search-notes

   cp skill-definitions/notion-create-note.md ~/.claude/skills/notion-create-note/SKILL.md
   cp skill-definitions/notion-edit-note.md ~/.claude/skills/notion-edit-note/SKILL.md
   cp skill-definitions/notion-list-project-notes.md ~/.claude/skills/notion-list-project-notes/SKILL.md
   cp skill-definitions/notion-read-note.md ~/.claude/skills/notion-read-note/SKILL.md
   cp skill-definitions/notion-search-notes.md ~/.claude/skills/notion-search-notes/SKILL.md
   ```

3. **Verify the installation**:
   ```bash
   ls -la ~/.claude/skills/
   ls -la ~/.claude/scripts/notion/
   ```

   You should see:
   - 5 skill directories in `~/.claude/skills/`
   - 7 Python scripts in `~/.claude/scripts/notion/`

### Step 6: Test the Installation

1. **Test the search functionality**:
   ```bash
   python3 ~/.claude/scripts/notion/search_notes.py --query "test" --limit 5
   ```

   If configured correctly, you should see JSON output with your notes (or an empty list if no matches).

2. **Test creating a note** (optional):
   ```bash
   python3 ~/.claude/scripts/notion/create_note.py --title "Test Note from Claude Code"
   ```

   Check your Notion Notes database - you should see the new note!

3. **Use in Claude Code**:
   - Open Claude Code
   - Try asking: "Search my Notion notes for [topic]"
   - Claude should automatically use the `notion-search-notes` skill

## 🚀 Usage

Once installed, the skills work automatically in Claude Code. Simply ask Claude to:

- **Create a note**: "Create a new note called 'Meeting Notes' with content about..."
- **Search notes**: "Find notes about API integration"
- **Read a note**: "Read the note called 'Project Planning'"
- **List project notes**: "Show me all notes in the 'Development' project"
- **Edit a note**: "Add a section about testing to my API notes"

Claude will automatically invoke the appropriate skill and parse the results.

### Example Conversations

```
You: "Find notes about server configuration"
Claude: [Uses notion-search-notes skill]
       Found 3 notes matching "server":
       1. Server Setup Guide
       2. Nginx Configuration
       3. SSL Certificate Notes
```

```
You: "Create a note called 'Daily Standup 2024-12-05' with today's updates"
Claude: [Uses notion-create-note skill]
       Created note "Daily Standup 2024-12-05" with 5 content blocks.
       View it here: [Notion URL]
```

## 🏗️ Architecture

```
~/.claude/
├── skills/
│   ├── notion-create-note/
│   │   └── SKILL.md
│   ├── notion-edit-note/
│   │   └── SKILL.md
│   ├── notion-list-project-notes/
│   │   └── SKILL.md
│   ├── notion-read-note/
│   │   └── SKILL.md
│   └── notion-search-notes/
│       └── SKILL.md
└── scripts/
    └── notion/
        ├── common.py                  # Shared utilities & config
        ├── create_note.py            # Create new note
        ├── edit_note.py              # Edit note content
        ├── list_project_notes.py     # List project notes
        ├── read_note.py              # Read note content
        ├── search_notes.py           # Search notes
        └── search_projects.py        # Find projects by name

/etc/keep-to-notion/
└── env.conf                          # Notion API token (secure)
```

### How It Works

1. **User asks Claude** to perform a Notion operation
2. **Claude identifies** the relevant skill based on the request
3. **Skill invokes** the corresponding Python script
4. **Script queries** the Notion API using your credentials
5. **Results return** as JSON to Claude
6. **Claude presents** the information in a readable format

## 🔧 Troubleshooting

### "Config file not found" Error

**Problem**: Script can't find `/etc/keep-to-notion/env.conf`

**Solution**:
```bash
sudo mkdir -p /etc/keep-to-notion
echo "NOTION_TOKEN=your_token_here" | sudo tee /etc/keep-to-notion/env.conf
sudo chmod 600 /etc/keep-to-notion/env.conf
```

### "API request failed" or Authentication Errors

**Problem**: Integration token is invalid or databases aren't shared

**Solutions**:
1. Verify token in `/etc/keep-to-notion/env.conf` matches your integration
2. Ensure you shared both Notes and Projects databases with your integration
3. Check token hasn't expired (regenerate if needed)

### "Database not found" Errors

**Problem**: Database IDs are incorrect

**Solutions**:
1. Double-check the database IDs in `~/.claude/scripts/notion/common.py`
2. Ensure IDs are formatted with dashes: `XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX`
3. Verify you're using the database ID from the URL, not the page ID

### Rate Limit Errors

**Problem**: Too many API requests too quickly

**Solution**: The scripts include 0.3s delays between requests. This is already compliant with Notion's limits. If you still get rate limit errors, the issue may be with other integrations or manual API usage.

### Notion API Quota (Free Accounts)

**Good news**: Notion's free tier is very generous for personal use! As of 2024:
- Free accounts get substantial API request quotas
- The built-in rate limiting (0.3s delays) ensures you stay within limits
- Typical usage of these skills won't hit quota limits

If you're concerned about quota, you can:
- Check your integration's usage at [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
- Upgrade to a paid plan for higher limits if needed

### Skills Not Appearing in Claude Code

**Problem**: Claude doesn't recognize the skills

**Solutions**:
1. Verify skill files are in `~/.claude/skills/notion-*/SKILL.md`
2. Check YAML frontmatter format in each SKILL.md file
3. Restart Claude Code
4. Try explicitly asking Claude to use a skill: "Use the notion-search-notes skill to find..."

## 🤝 Contributing

Contributions are welcome! If you'd like to:

- **Add new skills** (e.g., support for Tasks, Areas, Resources)
- **Fix bugs** or improve existing functionality
- **Enhance documentation**

Please open an issue or pull request on GitHub.

### Development Guidelines

1. Follow the existing code structure
2. Use `common.py` utilities for API calls
3. Ensure all scripts output JSON with `output_success()` or `output_error()`
4. Include comprehensive docstrings
5. Test with actual Notion data before submitting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Thomas Frank** for creating the Ultimate Brain Notion template
- **Anthropic** for Claude and Claude Code
- **Notion** for their excellent API

## 📞 Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review the [Notion API documentation](https://developers.notion.com/)
3. Open an issue on GitHub with:
   - Description of the problem
   - Error messages (remove sensitive data!)
   - Steps to reproduce

---

**Note**: This skills system is currently optimized for reading and managing **Notes** in the Ultimate Brain system. Support for Tasks and other database components may be added in future updates.

**Last updated**: 2024-12-05
