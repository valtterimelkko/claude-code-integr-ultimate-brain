# Workflow Configuration Guide

## Before You Import

These workflow files need to be configured with YOUR specific database IDs and optional customizations.

**What needs to be configured:**
1. **Database IDs** (Required - Notes and Projects)
2. **Webhook paths** (Optional - n8n can regenerate on import)
3. **File system paths** (Optional - if different from defaults)

**Time required:** 5-10 minutes for automated configuration, 15-20 minutes for manual

---

## Finding Your Database IDs

Before you can configure the workflows, you need your Notion database IDs.

### How to Find Them

1. **Open Notion** and go to your Ultimate Brain workspace
2. **Navigate to your Notes database**
3. **Copy the URL** from the browser:
   ```
   https://notion.so/workspace/YOUR-DATABASE-ID?v=...
   ```
4. **Extract the ID:** The long alphanumeric string after `workspace/` and before `?`
5. **Repeat for your Projects database**

### Example

If your URL is:
```
https://notion.so/workspace/2bf45010-ad5d-816a-8e25-f1f4d80a12a7?v=abc123
```

Your Database ID is:
```
2bf45010-ad5d-816a-8e25-f1f4d80a12a7
```

**Keep these IDs handy** - you'll need them in the next section.

---

## Option 1: Automatic Configuration (Recommended)

Use the provided Python script to automatically update all workflow files.

### Prerequisites

- Python 3.7+
- The script file: `configure_workflows.py`
- Your 7 workflow JSON files (includes 2 new workflows: archive-note and combine-notes)
- Your database IDs from above

### Run the Configuration Script

```bash
# Navigate to the workflows folder
cd claude-ai/n8n-workflows

# Run the configuration script
python3 configure_workflows.py \
  --notes-db "2bf45010-ad5d-816a-8e25-f1f4d80a12a7" \
  --projects-db "1234abcd-5678-efgh-ijkl-mnopqrstuvwx" \
  --output-dir ./configured
```

Replace the database IDs with your actual values.

### What It Does

1. **Reads** each workflow-*.json file (all 7)
2. **Finds** placeholder strings:
   - `YOUR_NOTES_DATABASE_ID_HERE`
   - `YOUR_PROJECTS_DATABASE_ID_HERE`
   - `/home/node/.claude/scripts/notion/`
3. **Replaces** them with your values
4. **Writes** new configured files to `./configured/` directory
5. **Shows** a confirmation of what changed

### Example Output

```
✅ Configured 7 workflows successfully!

Changes made:
  ✓ workflow-1-search-notes.json
    - Notes DB ID: 2bf45010-ad5d-816a-8e25-f1f4d80a12a7
    - Projects DB ID: 1234abcd-5678-efgh-ijkl-mnopqrstuvwx

  ✓ workflow-2-read-note.json
    - Notes DB ID: 2bf45010-ad5d-816a-8e25-f1f4d80a12a7

  ✓ workflow-3-list-project-notes.json
    - Projects DB ID: 1234abcd-5678-efgh-ijkl-mnopqrstuvwx

  ✓ workflow-4-create-note.json
    - Notes DB ID: 2bf45010-ad5d-816a-8e25-f1f4d80a12a7

  ✓ workflow-5-edit-note.json
    - Notes DB ID: 2bf45010-ad5d-816a-8e25-f1f4d80a12a7

  ✓ workflow-6-archive-note.json (NEW)
    - Notes DB ID: 2bf45010-ad5d-816a-8e25-f1f4d80a12a7

  ✓ workflow-7-combine-notes.json (NEW)
    - Notes DB ID: 2bf45010-ad5d-816a-8e25-f1f4d80a12a7

Ready to import files from: ./configured/
```

### Next Steps

1. All configured files are in `./configured/` folder
2. Go to n8n → **Workflows** → **Import**
3. Upload all 7 configured files
4. Skip to [Importing to n8n](#importing-to-n8n) section below

---

## Option 2: Manual Find & Replace

If you prefer manual control or the script doesn't work for you, here's the manual process.

### Step 1: Open the First Workflow File

```bash
# Use any text editor
nano claude-ai/n8n-workflows/workflow-1-search-notes.json
# or
code claude-ai/n8n-workflows/workflow-1-search-notes.json
```

### Step 2: Find and Replace Placeholders

Look for these exact strings and replace them:

**Search for:**
```
YOUR_NOTES_DATABASE_ID_HERE
```

**Replace with:** Your Notes database ID
```
2bf45010-ad5d-816a-8e25-f1f4d80a12a7
```

---

**Search for:**
```
YOUR_PROJECTS_DATABASE_ID_HERE
```

**Replace with:** Your Projects database ID
```
1234abcd-5678-efgh-ijkl-mnopqrstuvwx
```

---

**Search for:** (if different from defaults)
```
/home/node/.claude/scripts/notion/
```

**Replace with:** Your actual path in the container
```
/home/node/.claude/scripts/notion/
```

### Step 3: Validate JSON Syntax

After making changes, validate the JSON:

```bash
# Using Python
python3 -m json.tool workflow-1-search-notes.json > /dev/null && echo "✅ Valid JSON"

# Using jq (if installed)
jq empty workflow-1-search-notes.json && echo "✅ Valid JSON"
```

If you see `✅ Valid JSON`, it's correct. If not, check for:
- Missing quotes around strings
- Extra commas
- Mismatched brackets

### Step 4: Save with New Name

Save the file with a clear name:
```bash
mv workflow-1-search-notes.json workflow-1-search-notes.configured.json
```

### Step 5: Repeat for All 7 Workflows

Do this for all workflow files:
- `workflow-1-search-notes.json`
- `workflow-2-read-note.json`
- `workflow-3-list-project-notes.json`
- `workflow-4-create-note.json`
- `workflow-5-edit-note.json`
- `workflow-6-archive-note.json` (NEW)
- `workflow-7-combine-notes.json` (NEW)

### Step 6: Verify All Changes

```bash
# Check that placeholders are replaced in all files
grep -r "YOUR_NOTES_DATABASE_ID_HERE" .
grep -r "YOUR_PROJECTS_DATABASE_ID_HERE" .

# If you see no output, all placeholders are replaced ✅
```

---

## Importing to n8n

Once your workflows are configured (either automatically or manually):

### Step 1: Open n8n

Navigate to your n8n instance:
```
http://localhost:5678  (local)
https://n8n.yourdomain.com  (cloud)
```

### Step 2: Import Each Workflow

1. Click **Workflows** in the left sidebar
2. Click **Import** (or **+** button)
3. Select **Import from File**
4. Upload the first configured workflow file (e.g., `workflow-1-search-notes.json`)
5. n8n will import and show you the workflow structure
6. Click **Save** or **Activate** (depending on n8n version)
7. Repeat for all 7 workflow files

### Step 3: Verify Imports

After importing all 7 workflows:

1. Go to **Workflows** page
2. You should see all 7 listed:
   - search-notes
   - read-note
   - list-project-notes
   - create-note
   - edit-note
   - archive-note (NEW)
   - combine-notes (NEW)

3. For each workflow, verify:
   - **Status:** Shows "Inactive" (will be activated once tested)
   - **Trigger:** "Webhook" should be visible
   - **Nodes:** Should have multiple nodes (Webhook, Execute Command, etc.)

### Step 4: Test a Workflow

Test that the configuration worked:

1. **Open workflow 1** (search-notes)
2. Click the **Play** or **Execute** button
3. In the "Test" tab, enter:
   ```json
   {
     "query": "test",
     "limit": 5
   }
   ```
4. Run the test
5. Check the output - should return JSON with search results

**If successful:** ✅ Your configuration is correct!
**If error:** Check your database IDs and token (see [Troubleshooting](#troubleshooting) below)

### Step 5: Activate Workflows

Once tested:

1. For each workflow, click **Activate**
2. The workflow is now ready to be used by Claude.ai

---

## Troubleshooting Configuration

### "Invalid JSON" Error

**Cause:** JSON syntax error in the workflow file.

**Fix:**
1. Open the file in a text editor
2. Look for common issues:
   - Missing quotes: `"database_id": 2bf45010...` → should be `"database_id": "2bf45010..."`
   - Extra commas: `"field": "value",}` → remove the comma before }
   - Mismatched brackets: `{...]}` → should be `{...}`
3. Validate with: `python3 -m json.tool workflow-1-search-notes.json`

---

### "Database Not Found" Error

**Cause:** Database ID is incorrect or the token doesn't have access.

**Fix:**
1. **Double-check the database ID** in your Notion URL
2. **Verify the Notion token** in `/etc/keep-to-notion/env.conf`
3. **Check permissions:** The integration must be connected to the database in Notion
   - Open the database in Notion
   - Click **...** (top right) → **Connections**
   - Your integration should be listed

---

### "File Not Found" Error

**Cause:** Path to Python scripts is incorrect.

**Fix:**
1. In the workflow, find the Execute Command node
2. Check the path: `/home/node/.claude/scripts/notion/`
3. If different, update it to your actual path
4. Verify the path exists in your Docker container:
   ```bash
   docker-compose exec n8n ls /home/node/.claude/scripts/notion/
   ```

---

### Configure Script Fails

**Cause:** Script issues or incorrect usage.

**Fix:**
```bash
# Check Python version (need 3.7+)
python3 --version

# Run script with verbose output
python3 configure_workflows.py \
  --notes-db "YOUR_ID" \
  --projects-db "YOUR_ID" \
  --output-dir ./configured \
  --verbose

# Check that input files exist
ls -la workflow-*.json
```

---

## Next Steps

1. ✅ Configure your workflows (using Option 1 or Option 2)
2. ✅ Import them into n8n
3. ✅ Test at least one workflow
4. ✅ Activate all workflows
5. → Go to [Claude.ai + n8n Setup Guide](../SETUP_GUIDE.md#part-4-connecting-to-claudeai) to connect to Claude.ai

---

## Reference: Placeholder Locations

If you're editing JSON files manually, here are the placeholders and where they appear:

### workflow-1-search-notes.json
```json
{
  "nodes": [
    {
      "parameters": {
        "command": "python3 /home/node/.claude/scripts/notion/search_notes.py --database YOUR_NOTES_DATABASE_ID_HERE --query {{ $json.query }}"
      }
    }
  ]
}
```

### workflow-2-read-note.json
```json
{
  "nodes": [
    {
      "parameters": {
        "command": "python3 /home/node/.claude/scripts/notion/read_note.py --database YOUR_NOTES_DATABASE_ID_HERE --note-id {{ $json.note_id }}"
      }
    }
  ]
}
```

### workflow-3-list-project-notes.json
```json
{
  "nodes": [
    {
      "parameters": {
        "command": "python3 /home/node/.claude/scripts/notion/list_project_notes.py --database YOUR_PROJECTS_DATABASE_ID_HERE --project-id {{ $json.project_id }}"
      }
    }
  ]
}
```

### workflow-4-create-note.json
```json
{
  "nodes": [
    {
      "parameters": {
        "command": "python3 /home/node/.claude/scripts/notion/create_note.py --database YOUR_NOTES_DATABASE_ID_HERE --title {{ $json.title }}"
      }
    }
  ]
}
```

### workflow-5-edit-note.json

This workflow implements **unlimited content handling** via an internal file buffer approach:

1. **Convert to File Stream** - Converts the JSON content payload into a binary stream
2. **Write Temp File** - Writes the content to a temporary file with unique execution ID
3. **Run Python Script** - Calls `edit_note.py` with `--content-file` pointing to the temp file
4. **Cleanup** - Automatically removes the temporary file after execution
5. **Parse Output** - Converts Python JSON response to workflow output

This approach allows Claude to pass **arbitrarily large content** (entire documents, code files, research sections) without hitting bash ARG_MAX shell limits. The LLM is explicitly forbidden from summarizing or truncating content.

```json
{
  "nodes": [
    {
      "parameters": {
        "mode": "jsonToBinary",
        "sourceKey": "body.content",
        "convertAllData": false
      },
      "name": "Convert to File Stream",
      "type": "n8n-nodes-base.moveBinaryData"
    },
    {
      "parameters": {
        "fileName": "=/tmp/n8n_edit_{{ $executionId }}.txt",
        "dataPropertyName": "data"
      },
      "name": "Write Temp File",
      "type": "n8n-nodes-base.writeBinaryFile"
    },
    {
      "parameters": {
        "command": "=python3 /home/node/.claude/scripts/notion/edit_note.py --id \"{{ $json.body.id }}\" --action \"{{ $json.body.action }}\" --content-file /tmp/n8n_edit_{{ $executionId }}.txt && rm /tmp/n8n_edit_{{ $executionId }}.txt"
      },
      "name": "Run Python Script",
      "type": "n8n-nodes-base.executeCommand"
    }
  ]
}
```

### workflow-6-archive-note.json (NEW)
```json
{
  "nodes": [
    {
      "parameters": {
        "command": "python3 /home/node/.claude/scripts/notion/archive_note.py --id {{ $json.id }} --action {{ $json.action || 'archive' }}"
      }
    }
  ]
}
```

### workflow-7-combine-notes.json (NEW)
```json
{
  "nodes": [
    {
      "parameters": {
        "command": "python3 /home/node/.claude/scripts/notion/combine_notes.py --source-ids {{ $json.source_ids.join(' ') }}{{ $json.target_id ? ' --target-id ' + $json.target_id : '' }}{{ $json.create_new ? ' --create-new ' + $json.create_new : '' }}"
      }
    }
  ]
}
```

---

**Done configuring?** Head to the [Setup Guide](../SETUP_GUIDE.md) to continue! 🚀
