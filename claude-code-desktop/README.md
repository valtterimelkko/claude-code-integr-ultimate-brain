# Claude Code & Claude Desktop Integration

This folder contains all resources for integrating Ultimate Brain with **Claude Code** (VS Code extension) or **Claude Desktop** (native application).

## 🎯 What You Get

- **7 specialized Claude Code skills** to interact with your Notion
- **Local Python backend** - No cloud infrastructure needed
- **Works offline** - Once configured
- **Fast** - Direct local API calls
- **Secure** - Token stored in a user-local config file with permissions `600`

## 📋 Quick Start

**Option 1: Automated Installation (Recommended)**

```bash
cd claude-code-desktop
chmod +x install.sh
./install.sh
```

This script will:
1. Prompt for your database IDs and token
2. Write them to `~/.config/ultimate-brain-notion/env.conf` (or `$XDG_CONFIG_HOME`)
3. Copy files to `~/.claude/`
4. Set correct permissions
5. Run an offline import check without contacting Notion

**Option 2: Manual Installation**

See [Manual Installation](#manual-installation) section below.

**Estimated time:** ~5-10 minutes with automation, ~15-20 minutes manually

## 🚀 The 7 Skills

Once configured, Claude will have access to these tools:

1. **`notion_search_notes`** - Search your notes by keyword
2. **`notion_read_note`** - Read the full content of a note
3. **`notion_list_project_notes`** - See all notes in a project
4. **`notion_create_note`** - Create new notes in your Inbox
5. **`notion_edit_note`** - Append or modify existing notes (enhanced with long-form support)
6. **`notion_archive_note`** (NEW) - Archive or unarchive notes
7. **`notion_combine_notes`** (NEW) - Merge multiple notes into one

## 📂 What's Inside

### Scripts (`scripts/`)

- **`common.py`** - Shared utilities and API helpers
- **`config.py`** - User-local configuration loading with legacy fallback
- **`archive_note.py`** (NEW) - Archive or unarchive notes
- **`combine_notes.py`** (NEW) - Merge multiple notes into one
- **`create_note.py`** - Create new notes in Notion
- **`edit_note.py`** - Edit existing note content (enhanced)
- **`list_project_notes.py`** - List all notes in a project
- **`read_note.py`** - Read full note content
- **`search_notes.py`** - Search notes by keyword
- **`search_projects.py`** - Find projects by name

### Skill Definitions (`skill-definitions/`)

- **`notion-archive-note.md`** (NEW) - Archive note skill documentation
- **`notion-combine-notes.md`** (NEW) - Combine notes skill documentation
- **`notion-create-note.md`** - Create note skill documentation
- **`notion-edit-note.md`** - Edit note skill documentation (enhanced)
- **`notion-list-project-notes.md`** - List project notes skill documentation
- **`notion-read-note.md`** - Read note skill documentation
- **`notion-search-notes.md`** - Search notes skill documentation

### Tools

- **`install.sh`** - Automated installation script
- **`validate_config.py`** - Check that everything is configured correctly

## 🏗️ Installation Methods

### Automated Installation (Recommended)

```bash
cd claude-code-desktop
chmod +x install.sh
./install.sh
```

Follow the prompts to enter your database IDs and Notion token.

**What it does:**
1. Checks Python 3 and `requests` are installed
2. Prompts for your database IDs and Notion token
3. Writes a user-local config file outside the repository
4. Copies scripts to `~/.claude/scripts/notion/`
5. Copies skill definitions to `~/.claude/skills/notion-*/`
6. Verifies the installation without modifying the repository or making an API request

### Manual Installation

If you prefer manual control:

#### Step 1: Get Your Database IDs

1. Open your Ultimate Brain Notion workspace
2. Go to your Notes database
3. Copy the URL: `https://notion.so/workspace/YOUR-DATABASE-ID?v=...`
4. Extract the ID part (the long string) → This is your **Notes DB ID**
5. Repeat for your Projects database

#### Step 2: Create Configuration File

The scripts read database IDs and the token from a user-local file. This keeps
credentials and personal database identifiers out of the repository and makes
updating the installed copy safer.

```bash
mkdir -p "${XDG_CONFIG_HOME:-$HOME/.config}/ultimate-brain-notion"
cat > "${XDG_CONFIG_HOME:-$HOME/.config}/ultimate-brain-notion/env.conf" <<'EOF'
NOTES_DB_ID=your-notes-database-id
PROJECTS_DB_ID=your-projects-database-id
NOTION_TOKEN=secret_your_actual_token_here
EOF
chmod 600 "${XDG_CONFIG_HOME:-$HOME/.config}/ultimate-brain-notion/env.conf"
```

Set `NOTION_CONFIG_FILE` if you need a different location.

#### Step 4: Copy Files

```bash
# Create directories
mkdir -p ~/.claude/scripts/notion
mkdir -p ~/.claude/skills/notion-{search-notes,read-note,list-project-notes,create-note,edit-note}

# Copy scripts
cp scripts/*.py ~/.claude/scripts/notion/

# Copy skill definitions
cp skill-definitions/notion-*.md ~/.claude/skills/notion-*/SKILL.md
```

#### Step 5: Verify Installation

```bash
python3 validate_config.py
```

Should show all checks passing ✅

## 🔧 Validate Your Configuration

After installation, verify everything is configured:

```bash
python3 validate_config.py
```

This checks:
- ✅ Database IDs are configured
- ✅ Python scripts are installed
- ✅ Skill definitions are in place
- ✅ Notion token is accessible
- ✅ Can connect to Notion API

## 🧪 Test Your Installation

After verification passes, test that everything works:

```bash
# Test 1: Search for notes (should return JSON)
python3 ~/.claude/scripts/notion/search_notes.py --query "test" --limit 5

# Test 2: List projects
python3 ~/.claude/scripts/notion/search_projects.py --name "YOUR_PROJECT" --limit 5
```

Both should return valid JSON responses. If they do, you're ready to use Claude!

## 🚀 Using Your Skills

### In Claude Code (VS Code)

1. **Restart VS Code** after installation
2. **Open a chat** with Claude Code
3. Claude should show your 5 skills in the tool list
4. **Try asking:**
   - "Search my notes for API design"
   - "Show me all notes in the DevOps project"
   - "Create a note titled 'Quick reminder' with content 'Remember this'"

### In Claude Desktop

1. **Restart Claude Desktop** after installation
2. **Open a chat**
3. Claude should show your 5 skills
4. **Try using them** in your conversation

## 📊 How It Works (Visual)

```
┌──────────────┐
│  Claude Code │
│  or Desktop  │
└──────┬───────┘
       │ Uses skills
       ▼
┌──────────────────────┐
│  5 Claude Code Skills │ (notion-search-notes, etc.)
└──────┬───────────────┘
       │ Calls Python scripts
       ▼
┌──────────────────────┐
│   Python Scripts     │ (search_notes.py, etc.)
└──────┬───────────────┘
       │ Reads config
       ▼
┌──────────────────────┐
│  env.conf config     │ (IDs and token)
└──────┬───────────────┘
       │ Makes API calls
       ▼
┌──────────────────────┐
│   Notion API         │
│  (api.notion.com)    │
└──────┬───────────────┘
       │ Returns data
       ▼
┌──────────────────────┐
│ Your Notion Data     │
│ (Notes & Projects)   │
└──────────────────────┘
```

## 🐛 Troubleshooting

### "Skills not showing in Claude"

**Solution:**
1. Make sure `install.sh` ran without errors
2. Restart Claude Code (VS Code) or Claude Desktop completely
3. Run `python3 validate_config.py` to check configuration
4. Check that files exist: `ls ~/.claude/skills/notion-*/SKILL.md`

### "Database not found" or "API Error"

**Solution:**
1. Verify your database IDs are correct
2. Check your Notion token hasn't expired
3. Make sure the integration is connected to the databases in Notion:
   - Open the database in Notion
   - Click **...** (top right) → **Connections**
   - Your integration should be listed
4. Run: `python3 validate_config.py` for detailed diagnostics

### "Permission denied" errors

**Solution:**
1. Check file permissions:
   ```bash
   ls -la "${XDG_CONFIG_HOME:-$HOME/.config}/ultimate-brain-notion/env.conf"
   # Should show: -rw------- (not just -rw-r--r--)
   ```
2. If wrong, fix permissions:
   ```bash
   chmod 600 "${XDG_CONFIG_HOME:-$HOME/.config}/ultimate-brain-notion/env.conf"
   ```

### "Module not found" or "requests" error

**Solution:**
```bash
# Install the requests library
pip3 install requests

# Then run installation again
./install.sh
```

## 🔐 Security Notes

- Your Notion token and database IDs are stored in the user-local config file with restricted permissions (600)
- The installer does not write credentials into the repository or mutate its source scripts
- A legacy `/etc/keep-to-notion/env.conf` file is read only as a compatibility fallback
- Scripts execute locally on your machine
- No data is sent to external servers except Notion's API

## ✅ Compatibility

✅ **Claude Code** (VS Code extension)
✅ **Claude Desktop** (native application)
✅ **macOS** (Intel & Apple Silicon)
✅ **Linux** (Ubuntu, Debian, etc.)
✅ **Windows (WSL2)** (Windows Subsystem for Linux)

## 💡 Comparison: Claude Code vs Claude.ai

| Feature | Claude Code/Desktop | Claude.ai + n8n |
|---------|---------------------|-----------------|
| Setup | Local installation | Web-based |
| Installation Time | ~10 minutes | ~30 minutes |
| Offline Support | Yes | No |
| Scheduled Tasks | No | Yes |
| Team Collaboration | No | Yes |
| Configuration | Local file | Web interface |
| Cost | Free (included with subscription) | Free tier available |

## 📚 Next Steps

1. ✅ Run `./install.sh` (or follow manual steps)
2. ✅ Verify with `python3 validate_config.py`
3. ✅ Test scripts: `python3 ~/.claude/scripts/notion/search_notes.py --query "test" --limit 5`
4. ✅ Restart Claude Code or Claude Desktop
5. ✅ Try using your skills in a chat!

## 💬 Need Help?

- **Installation issues?** → Check [Troubleshooting](#-troubleshooting)
- **Want to compare approaches?** → See [Comparison](#-comparison-claude-code-vs-claudeai)
- **Have questions?** → See [../README.md](../README.md#support)
