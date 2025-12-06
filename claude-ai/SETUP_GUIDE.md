# Claude.ai + n8n Setup Guide

## Quick Start (Choose Your Path)

**Do you have n8n already?**
- **Yes** → Jump to [Phase 3: Docker Environment Setup](#phase-3-docker-environment-setup)
- **No** → Start with [Phase 1: Notion Setup](#phase-1-notion-setup)

**Estimated Time:**
- New to n8n: ~30 minutes
- Already have n8n: ~15 minutes

---

## Part 1: Understanding the System

### What is this System?

This workflow is a comprehensive **Instance-Level MCP Bridge** that connects **Claude.ai** directly to your **Notion Ultimate Brain** system.

Unlike standard integrations that treat Notion as a single generic destination, this system gives Claude "Agentic" capabilities by breaking down interactions into **5 distinct, specialized tools**. This allows Claude to reason like a human operator: *"I should search for the project first, read the relevant notes to understand the context, and only then add a new note."*

### Key Value Delivered

* **Precision over Guesswork:** Because Search, Read, and Edit are separate tools, Claude doesn't blindly hallucinate note IDs or overwrite content. It creates a feedback loop where it can "look before it leaps."
* **Context-Aware Documentation:** The `list_project_notes` tool allows Claude to instantly download the entire "context" of a project before answering your questions, effectively giving it long-term memory of your specific work history.
* **Safety & Control:** "Inbox Zero" philosophy is built-in. New notes are created in the **Inbox** (unrelated to projects) by default, ensuring the AI doesn't misfile documents deep in your database. You remain the final organizer.
* **Complex Editing:** The `edit_note` tool supports advanced operations like appending specific code blocks to an existing technical guide, preserving the original formatting—something generic integrations often fail at.

### The Tool Suite (What Claude Sees)

When you connect, Claude sees these 5 tools in its toolbox:

1. **`notion_search_notes`**: The "Eyes." Finds Note IDs by title or keyword.
2. **`notion_read_note`**: The "Brain." Reads full Markdown content of a specific note.
3. **`notion_list_project_notes`**: The "Map." Lists all notes linked to a specific Project ID.
4. **`notion_create_note`**: The "Pen." Creates new notes in the Inbox.
5. **`notion_edit_note`**: The "Editor." Appends or modifies existing note content.

### How Claude Uses These Tools

Claude can:
- Search for information across your Notion workspace
- Read full notes to understand context
- List all notes in a specific project for complete context
- Create new notes in your Inbox for capture
- Edit existing notes to append insights or updates

This agentic approach means Claude can reason through problems step-by-step, checking facts and building context as it goes.

---

## Part 2: Prerequisites Checklist

Before you begin, make sure you have:

- [ ] **n8n Version 1.122.5+** (Required for MCP support)
  - Check your n8n version in the bottom-left corner of the dashboard
  - If older, you'll need to update: `docker pull docker.n8n.io/n8nio/n8n:1.122.5`

- [ ] **Notion Workspace Access**
  - You must be a workspace admin to create integrations

- [ ] **Notion Internal Integration Token**
  - Create one at [Notion My Integrations](https://www.notion.so/my-integrations)
  - Keep this secret! It has full access to your workspace

- [ ] **Database IDs for Notes and Projects**
  - Find these in your Notion workspace
  - See [Finding Your Database IDs](#finding-your-database-ids) below

- [ ] **Docker & Docker Compose** (if self-hosting n8n)
  - For cloud-hosted n8n, this is handled for you

- [ ] **Basic command-line familiarity**
  - You'll run a few bash commands

### Finding Your Database IDs

In Notion:
1. Open your Notes database
2. Copy the URL: `https://notion.so/workspace/YOUR-DATABASE-ID?v=...`
3. Extract the part after `workspace/` and before `?` → That's your Notes DB ID
4. Repeat for your Projects database

Example: `2bf45010-ad5d-816a-8e25-f1f4d80a12a7`

---

## Part 3: Installation Steps

### Phase 1: Notion Setup (Getting Credentials)

Unlike standard n8n workflows, this system uses **file-based authentication** for the Python scripts. You do **not** need to add a credential inside the n8n UI.

#### Step 1: Create Integration

1. Go to [Notion My Integrations](https://www.notion.so/my-integrations)
2. Click **New integration**
3. Name it (e.g., "Claude Brain Access")
4. Select your workspace and submit
5. **Copy the "Internal Integration Secret"** (starts with `secret_...`)
6. Store it safely - we'll use it in Step 3

#### Step 2: Connect Databases

1. Open your **Notes Database** in Notion
2. Click the **...** menu (top right) → **Connections** → Select your new integration
3. Repeat this for your **Projects Database**

This gives the integration permission to read and write to these databases.

---

### Phase 2: File System & Permissions

You need a persistent place on your **Host Server** to store the scripts and credentials so the Docker container can access them.

#### Step 1: Create Directory Structure

Decide where to keep your n8n files on the host. In this guide, we'll use `~/n8n-docker/` as an example.

```bash
# Create directories
mkdir -p ~/n8n-docker/local_files/notion
sudo mkdir -p /etc/keep-to-notion
```

#### Step 2: Deploy Scripts

1. Copy all Python script files into the notion directory:
```bash
cp claude-code-desktop/scripts/*.py ~/n8n-docker/local_files/notion/
```

These scripts should be in place:
- `common.py`
- `search_notes.py`
- `read_note.py`
- `list_project_notes.py`
- `create_note.py`
- `edit_note.py`

#### Step 3: Configure Credentials

Create the config file with your Notion token:

```bash
sudo nano /etc/keep-to-notion/env.conf
```

Add this line (replace with your actual token):
```
NOTION_TOKEN=secret_your_token_here_abc123...
```

Save and close the file.

#### Step 4: Set Correct Permissions (CRITICAL!)

Files created with `sudo` often default to root-only access. The n8n container runs as user `node` (UID 1000) and needs to read this file:

```bash
sudo chmod 644 /etc/keep-to-notion/env.conf
```

Verify it worked:
```bash
ls -la /etc/keep-to-notion/env.conf
# Should show: -rw-r--r-- (not just ---r----)
```

---

### Phase 3: Docker Environment Setup

We must customize the n8n container to include Python dependencies and ensure the correct version is running.

#### Step 1: Create Custom Dockerfile

In your `~/n8n-docker/` directory, create a file named `Dockerfile`:

```dockerfile
# IMPORTANT: Ensure version is 1.122.5 or higher for MCP support
FROM docker.n8n.io/n8nio/n8n:1.122.5

USER root
# Install Python3, Pip, and Requests library
RUN apk add --no-cache python3 py3-pip py3-requests

USER node
```

#### Step 2: Update docker-compose.yml

Create or update your `docker-compose.yml` file with proper volume mounts:

```yaml
version: '3.8'

services:
  n8n:
    build:
      context: .
      dockerfile: Dockerfile

    ports:
      - "5678:5678"

    environment:
      - N8N_HOST=${N8N_HOST:-localhost}
      - N8N_PORT=${N8N_PORT:-5678}
      - N8N_PROTOCOL=${N8N_PROTOCOL:-http}
      - NODE_ENV=production

    volumes:
      # Mount 1: The Scripts (Host Path -> Container Path)
      - ./local_files/notion:/home/node/.claude/scripts/notion

      # Mount 2: The Credentials (read-only)
      - /etc/keep-to-notion/env.conf:/etc/keep-to-notion/env.conf:ro

      # Standard n8n data
      - n8n_data:/home/node/.n8n

    restart: unless-stopped

volumes:
  n8n_data:
```

**Important:** Do not change the container-side paths (`/home/node/.claude/...`). The scripts are hardcoded to expect this structure.

#### Step 3: Rebuild and Launch

From your `~/n8n-docker/` directory:

```bash
docker-compose up -d --build
```

This will:
1. Build the custom image with Python dependencies
2. Start the n8n container
3. Mount the script and credential files

Check that it started:
```bash
docker-compose logs n8n | grep "n8n ready on"
```

---

### Phase 4: Workflow Configuration

#### Step 1: Import Workflows

1. Open your n8n instance (usually `http://localhost:5678`)
2. Go to **Workflows** → **Import**
3. Upload each of these 5 JSON files:
   - `workflow-1-search-notes.json`
   - `workflow-2-read-note.json`
   - `workflow-3-list-project-notes.json`
   - `workflow-4-create-note.json`
   - `workflow-5-edit-note.json`

#### Step 2: Configure Database IDs

Before using the workflows, you must update the placeholder database IDs.

**Option A: Automatic Configuration (Recommended)**

Use the provided configuration script:

```bash
cd claude-ai/n8n-workflows
python3 configure_workflows.py \
  --notes-db "YOUR_NOTES_DATABASE_ID" \
  --projects-db "YOUR_PROJECTS_DATABASE_ID" \
  --output-dir ./configured
```

This creates ready-to-import files in the `./configured/` folder.

**Option B: Manual Find & Replace**

If you prefer manual control:

1. Open the first workflow JSON file in a text editor
2. Find these placeholders:
   - `YOUR_NOTES_DATABASE_ID_HERE` → Replace with your Notes DB ID
   - `YOUR_PROJECTS_DATABASE_ID_HERE` → Replace with your Projects DB ID
3. Save the file with a new name (e.g., `workflow-1-configured.json`)
4. Import the configured file to n8n
5. Repeat for all 5 workflow files

#### Step 3: Verify MCP Settings

For each workflow:

1. Open the workflow in n8n
2. Open the **Webhook Node** (usually the first node)
3. Ensure **"Available for MCP"** is toggled **ON**
4. Verify the **Input Schema** matches the tool:
   - `notion_search_notes` should have `query` field
   - `notion_read_note` should have `note_id` field
   - etc.

#### Step 4: Verify Execution Path

For each workflow:

1. Open the **Execute Command** node
2. Verify the command points to the correct path:
   ```
   python3 /home/node/.claude/scripts/notion/search_notes.py ...
   ```

---

## Part 4: Connecting to Claude.ai

### Step 1: Get Your MCP Server URL

1. Open your n8n instance
2. Go to **Settings** (bottom-left corner)
3. Look for **MCP** or **Model Context Protocol** section
4. Copy your **MCP Server URL** (e.g., `https://n8n.yourdomain.com/mcp`)

### Step 2: Add MCP Server to Claude.ai

1. Go to [Claude.ai](https://claude.ai)
2. Open a chat or go to **Project Settings**
3. Look for **Tools** or **MCP Servers**
4. Click **Add MCP Server**
5. Paste your n8n MCP URL
6. If your n8n requires authentication, provide username/password or token
7. Save and verify connection

### Step 3: Verify Tools Are Available

Claude should now show you these tools:
- `notion_search_notes` - Search your notes
- `notion_read_note` - Read a specific note
- `notion_list_project_notes` - List notes in a project
- `notion_create_note` - Create a new note
- `notion_edit_note` - Edit a note

Test by saying: *"Search my notes for API design"*

---

## Part 5: Troubleshooting

### Common Errors & Solutions

#### "Project 'XXX' not found" (when it definitely exists)

**Cause:** The script cannot read the token file due to permissions, so the API call fails silently.

**Fix:**
```bash
sudo chmod 644 /etc/keep-to-notion/env.conf
sudo chmod 755 /etc/keep-to-notion
```

Then restart n8n:
```bash
docker-compose restart n8n
```

---

#### "ModuleNotFoundError: No module named 'requests'"

**Cause:** The custom Dockerfile didn't build or wasn't used.

**Fix:**
```bash
# Rebuild with the custom Dockerfile
docker-compose up -d --build

# Verify Python is available in the container
docker-compose exec n8n python3 --version
```

---

#### "Claude says 'No tools available'"

**Cause:** n8n version is too old (needs 1.122.5+).

**Fix:**
1. Check your n8n version in the bottom-left dashboard corner
2. If older, update your `Dockerfile`:
   ```dockerfile
   FROM docker.n8n.io/n8nio/n8n:1.122.5
   ```
3. Rebuild: `docker-compose up -d --build`
4. Verify: Check dashboard version again

---

#### "Permission denied" when reading credential file

**Cause:** File permissions are too restrictive.

**Fix:**
```bash
# Make readable by the node user
sudo chmod 644 /etc/keep-to-notion/env.conf

# Make directory accessible
sudo chmod 755 /etc/keep-to-notion

# Verify
ls -la /etc/keep-to-notion/
```

---

#### "n8n can't reach the Notion API"

**Cause:** Token is invalid or expired.

**Fix:**
1. Get a fresh token from [Notion My Integrations](https://www.notion.so/my-integrations)
2. Update `/etc/keep-to-notion/env.conf`:
   ```bash
   sudo nano /etc/keep-to-notion/env.conf
   # Update the token
   ```
3. Restart n8n:
   ```bash
   docker-compose restart n8n
   ```

---

#### "Workflows won't import (JSON error)"

**Cause:** Database ID placeholders weren't updated.

**Fix:**
1. Run the configuration script (see [Phase 4, Step 2](#step-2-configure-database-ids))
2. Or manually edit the JSON files to replace placeholders
3. Try importing again

---

### Advanced Troubleshooting

#### Check Container Logs

```bash
docker-compose logs -f n8n
```

Look for error messages and search the n8n documentation.

#### Verify Script Execution

Test a script manually in the container:

```bash
docker-compose exec n8n python3 /home/node/.claude/scripts/notion/search_notes.py --query "test" --limit 5
```

Should return valid JSON if everything is configured correctly.

#### Check File Mounts

Verify files are mounted correctly:

```bash
# Check if scripts are mounted
docker-compose exec n8n ls -la /home/node/.claude/scripts/notion/

# Check if config is readable
docker-compose exec n8n cat /etc/keep-to-notion/env.conf
```

---

## Part 6: Next Steps

### Once Everything Is Working

1. **Test with Claude:** Ask Claude to search, read, and create notes
2. **Create Workflows:** Use n8n's visual editor to build custom automations
3. **Set Up Schedules:** Make workflows run automatically on a schedule
4. **Share with Team:** If using cloud n8n, invite team members

### Documentation References

- [n8n Documentation](https://docs.n8n.io/)
- [Notion API Reference](https://developers.notion.com/reference)
- [Claude.ai Model Context Protocol](https://github.com/modelcontextprotocol)

### Need Help?

- Check the [Troubleshooting section](#part-5-troubleshooting) above
- Review the workflow files to understand how they work
- Check your n8n container logs: `docker-compose logs n8n`
- See the main repository [Support section](../README.md#support)

---

**You're all set!** Start using Claude with your Ultimate Brain. 🚀
