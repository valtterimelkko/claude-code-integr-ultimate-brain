# Claude.ai Integration with n8n

Welcome! This folder contains everything needed to integrate your **Ultimate Brain** with **Claude.ai** using **n8n** workflow automation.

## 🎯 What You Get

- **7 specialized tools** Claude can use to interact with your Notion
- **Web-based automation** - No local installation required
- **Scheduled workflows** - Run tasks on a schedule or trigger them manually
- **Team collaboration** - Share workflows with team members
- **Visual workflow builder** - Design automations graphically

## 📋 Quick Start

**Choose your path:**

1. **I already have n8n** → Jump to [Setup Guide: Phase 3](./SETUP_GUIDE.md#phase-3-docker-environment-setup)
2. **I need to set up n8n first** → Start with [Setup Guide: Phase 1](./SETUP_GUIDE.md#phase-1-notion-setup-getting-credentials)
3. **Just tell me how it works** → Read [Understanding the System](./SETUP_GUIDE.md#part-1-understanding-the-system)

**Estimated time:**
- New to n8n: **~30 minutes**
- Already have n8n: **~15 minutes**

## 📂 What's Inside

- **[SETUP_GUIDE.md](./SETUP_GUIDE.md)** - Complete step-by-step installation and configuration guide
- **[n8n-workflows/](./n8n-workflows/)** - Pre-built workflow files ready to import
  - **CONFIGURATION_GUIDE.md** - How to configure workflows with your database IDs
  - **configure_workflows.py** - Automatic configuration script
  - **7 workflow JSON files** - Ready-to-import workflows

## 🔧 The 7 Tools Claude Can Use

1. **`notion_search_notes`** - Search your notes by keyword
2. **`notion_read_note`** - Read the full content of any note
3. **`notion_list_project_notes`** - See all notes in a specific project
4. **`notion_create_note`** - Create new notes in your Inbox
5. **`notion_edit_note`** - Append or modify existing note content (unlimited length via file buffers)
6. **`notion_archive_note`** (NEW) - Archive or unarchive notes
7. **`notion_combine_notes`** (NEW) - Merge multiple notes into one

## 🚀 Next Steps

1. **Read the [Setup Guide](./SETUP_GUIDE.md)** - Covers all 4 phases of setup
2. **Configure your workflows** - See [n8n-workflows/CONFIGURATION_GUIDE.md](./n8n-workflows/CONFIGURATION_GUIDE.md)
3. **Import to n8n** - Follow the instructions in the Setup Guide
4. **Connect to Claude.ai** - One simple step in the Setup Guide
5. **Start using it!** - Ask Claude to search, read, and manage your notes

## 💡 Why Use This Instead of Claude Code/Desktop?

| Feature | Claude Code/Desktop | Claude.ai + n8n |
|---------|---------------------|-----------------|
| Setup Required | Yes (local installation) | No (web-based) |
| Collaboration | Personal use only | Team workflows |
| Real-time Chat | Limited integration | Full integration |
| Scheduled Tasks | Manual triggering | Built-in scheduling |
| Maintenance | Local configuration | Cloud-based (n8n handles it) |
| Cost | Included with Claude | n8n free tier or self-hosted |
| Network | Works offline | Requires internet |

## 🤔 Not Sure Which One to Use?

- **Use Claude Code/Desktop if:** You prefer working locally, want offline support, or use VS Code
- **Use Claude.ai + n8n if:** You want web-based workflows, team collaboration, or scheduled automation

You can use both! They access the same Notion data.

## 💬 Need Help?

- **Check the [Setup Guide Troubleshooting section](./SETUP_GUIDE.md#part-5-troubleshooting)**
- **Review the [Configuration Guide](./n8n-workflows/CONFIGURATION_GUIDE.md)**
- **See the main repository [Support section](../README.md#support)**

---

**Ready to start?** → Go to the [Setup Guide](./SETUP_GUIDE.md) 🚀
