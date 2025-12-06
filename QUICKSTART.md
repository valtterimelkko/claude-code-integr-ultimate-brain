# Ultra-Quick Start Guide

**For experienced developers who want to jump in fast.**

Choose your platform and follow the accelerated setup below. These instructions skip detailed explanations—see the full guides for more context.

---

## Claude Code/Desktop (10 minutes)

### Prerequisites
- Python 3.7+
- `requests` library (`pip3 install requests`)
- Your Notion Notes and Projects database IDs
- Your Notion integration token

### Installation

```bash
# Clone/navigate to repo
cd claude-code-desktop

# Make script executable
chmod +x install.sh

# Run automated installation
./install.sh
```

**When prompted:**
1. Enter your Notes database ID
2. Enter your Projects database ID
3. Enter your Notion integration token

**Verify:**
```bash
python3 validate_config.py
```

All checks should pass ✅

**Done!** Restart Claude Code or Claude Desktop. Your 5 skills are ready:
- notion_search_notes
- notion_read_note
- notion_list_project_notes
- notion_create_note
- notion_edit_note

### Test It

```bash
# Search for notes
python3 ~/.claude/scripts/notion/search_notes.py --query "test" --limit 5

# Ask Claude
# "Search my notes for API design"
```

---

## Claude.ai + n8n (30 minutes - or 15 if you already have n8n)

### Prerequisites
- n8n instance running (v1.122.5+)
  - Cloud: [n8n Cloud](https://n8n.cloud) (free tier available)
  - Self-hosted: `docker-compose up` with provided Dockerfile
- Your Notion integration token
- Your database IDs
- Claude.ai account

### Quick Setup

#### 1. Prepare Your n8n Instance

**If using cloud n8n:**
- Skip Docker setup, just ensure it's running

**If self-hosting:**
```bash
# Create directory
mkdir -p ~/n8n-docker/local_files/notion

# Copy scripts
cp claude-code-desktop/scripts/*.py ~/n8n-docker/local_files/notion/

# Create Dockerfile (use the one from claude-ai/SETUP_GUIDE.md)
# Create docker-compose.yml (use the one from claude-ai/SETUP_GUIDE.md)

# Start n8n
docker-compose up -d --build
```

#### 2. Configure Credentials

```bash
# Create config directory
sudo mkdir -p /etc/keep-to-notion

# Add Notion token
echo "NOTION_TOKEN=secret_your_token_here" | sudo tee /etc/keep-to-notion/env.conf

# Set permissions
sudo chmod 600 /etc/keep-to-notion/env.conf
```

#### 3. Configure Workflows

```bash
cd claude-ai/n8n-workflows

# Run configuration script
python3 configure_workflows.py \
  --notes-db "YOUR_NOTES_DB_ID" \
  --projects-db "YOUR_PROJECTS_DB_ID" \
  --output-dir ./configured
```

#### 4. Import Workflows

1. Open n8n → **Workflows** → **Import**
2. Upload all 5 files from `./configured/` folder
3. For each workflow, toggle **"Available for MCP"** ON

#### 5. Connect to Claude.ai

1. Open n8n settings → find **MCP** section
2. Copy your MCP Server URL
3. Go to Claude.ai → **Project Settings** → **Tools**
4. Click **Add MCP Server** → paste your n8n URL
5. Verify: Claude should list the 5 tools

**Done!** Start asking Claude to search, read, and create notes via n8n.

### Test It

Ask Claude.ai:
```
"Search my notes for API"
"Create a note about today's standup"
"Show me all notes in the DevOps project"
```

---

## Common Questions

### Where do I find my database IDs?

Notion URL: `https://notion.so/workspace/YOUR-DATABASE-ID?v=...`

Extract the long string between `workspace/` and `?`

### Where do I get my integration token?

1. Go to [Notion My Integrations](https://www.notion.so/my-integrations)
2. Create new integration
3. Copy the "Internal Integration Secret" (starts with `secret_...`)

### Which platform should I use?

- **Claude Code:** Fast, local, offline
- **Claude.ai + n8n:** Automated workflows, scheduling, web-based

Or use both! They access the same Notion data.

### Can I switch platforms later?

Yes! Both platforms use your same database IDs. You can install both and use whichever fits each use case.

### What if something goes wrong?

See full troubleshooting guides:
- Claude Code: `claude-code-desktop/README.md#-troubleshooting`
- Claude.ai: `claude-ai/SETUP_GUIDE.md#part-5-troubleshooting`

Or run validation:
```bash
# Claude Code
python3 claude-code-desktop/validate_config.py

# Claude.ai
# Check workflow configuration section
```

---

## Next Steps

1. ✅ Choose your platform
2. ✅ Follow the accelerated steps above
3. ✅ Verify installation works
4. ✅ Start using with Claude!

**Need more details?** → See full guides in `claude-code-desktop/README.md` or `claude-ai/SETUP_GUIDE.md`

---

**Last updated:** 2024-12-06
