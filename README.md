# Ultimate Brain AI Integration Toolkit

A comprehensive toolkit that enables seamless integration between **Thomas Frank's Ultimate Brain** Notion workspace and AI platforms—from Claude Code/Desktop to Claude.ai with n8n automation. Access your knowledge base and automate workflows across multiple platforms without extra costs or data duplication.

## 🌐 Multiple Platforms, One Source of Truth

Choose your integration approach:

- **💻 Claude Code & Claude Desktop** - Direct integration with VS Code extension or native app
- **🌐 Claude.ai + n8n** - Web-based automation workflows with Claude

All integrations access the same Notion source of truth with structured, efficient API queries.

## 🚀 Quick Start: Choose Your Path

| I want to... | Choose This | Time | Setup |
|--------------|-------------|------|-------|
| Use Claude in VS Code or native app | [Claude Code/Desktop](claude-code-desktop/README.md) | ~10 min | Local installation |
| Automate workflows with web Claude | [Claude.ai + n8n](claude-ai/README.md) | ~30 min | Web-based setup |
| Learn more before deciding | Read [below](#why-this-matters) | 5 min | Just reading |

## 💡 Why This Matters: The Value Proposition

If you're already using [Ultimate Brain](https://thomasjfrank.com/brain/) to organize your projects, notes, and knowledge, these skills unlock powerful AI-first workflows:

### 🔍 **AI-First Information Access**
- **Find and retrieve** your information at speed using natural language instead of manual Notion navigation
- **Quick edits** to your knowledge base without context-switching away from your AI workflow
- Search and access your notes and projects as part of agentic conversations, making your data immediately actionable

### 🎯 **Ultimate Brain as Your Source of Truth**
- Use your **Projects database as the authoritative context** for AI-powered work
- Feed project details, goals, and requirements directly to Claude for:
  - Content creation informed by your actual projects
  - Code generation grounded in your technical specifications
  - Strategic planning based on your documented context
  - Task decomposition from your project structure

### 🧠 **Context Engineering Without Extra Cost**
- **Leverage AI as a productivity multiplier** without paying for Notion's AI add-ons
- Perfect if you already subscribe to Claude, ChatGPT, or other AI services
- Your Ultimate Brain becomes the "knowledge base" that powers better AI responses
- **Context is everything in AI workflows** — structured, organized context (like Ultimate Brain provides) means higher quality, more relevant AI outputs

### 🚀 **Seamless AI Integration**
- **No data duplication**: Access your single source of truth directly
- **Stay in control**: All your data remains in Notion under your management
- **Rate-limit friendly**: Built-in delays ensure sustainable, respectful API usage
- **Privacy focused**: Your integration token stays secure on your machine or in n8n

This approach transforms Ultimate Brain from a passive information store into an **active intelligence layer** for your AI-powered work.

---

## 📚 Platform-Specific Guides

### For Claude Code/Desktop Users

**What you get:**
- Works with Claude Code (VS Code extension) or Claude Desktop
- Local Python scripts that query your Notion directly
- Real-time access to your notes and projects
- No extra services needed

**Setup time:** ~10 minutes (automated) or ~20 minutes (manual)

→ **[Go to Claude Code/Desktop Setup Guide](claude-code-desktop/README.md)**

Quick preview:
```bash
cd claude-code-desktop
chmod +x install.sh
./install.sh
# Answer a few questions about your database IDs
# Done! Restart Claude Code and start using the 5 skills
```

### For Claude.ai + n8n Users

**What you get:**
- Web-based automation with Claude.ai
- Visual workflow builder
- Scheduled task execution
- Easy team collaboration
- Free tier available

**Setup time:** ~30 minutes

→ **[Go to Claude.ai + n8n Setup Guide](claude-ai/SETUP_GUIDE.md)**

Quick preview:
1. Set up n8n (cloud or self-hosted)
2. Configure your Notion databases
3. Import the 5 pre-built workflows
4. Connect to Claude.ai via MCP
5. Start automating!

---

## ⚡ Available Capabilities

Both platforms provide access to these 5 core operations:

1. **Search Notes** - Find notes by keyword or project
2. **Read Notes** - Get full content of any note
3. **List Project Notes** - See all notes in a specific project
4. **Create Notes** - Add new notes to your brain
5. **Edit Notes** - Append or modify existing content

---

## ✅ Prerequisites

### Common (Both Platforms)
- **Ultimate Brain Notion workspace** set up and working
- **Notion integration token** from your workspace
- **Database IDs** for your Notes and Projects databases
- Basic command-line familiarity

### Platform-Specific
- **Claude Code:** Python 3.7+, VS Code or Claude Desktop installed
- **Claude.ai:** n8n instance (cloud free tier or self-hosted), basic Docker knowledge

→ **See your chosen platform's guide for detailed setup**

---

## 🏗️ Repository Structure

```
ultimate-brain-ai-integration/
│
├── 📁 claude-code-desktop/
│   ├── README.md                    # Setup & configuration guide
│   ├── install.sh                   # Automated installation
│   ├── validate_config.py           # Configuration checker
│   ├── scripts/                     # Python backend
│   │   ├── common.py               # Shared utilities & config
│   │   ├── search_notes.py
│   │   ├── read_note.py
│   │   ├── list_project_notes.py
│   │   ├── create_note.py
│   │   ├── edit_note.py
│   │   └── search_projects.py
│   └── skill-definitions/           # Claude Code skill files
│
├── 📁 claude-ai/
│   ├── README.md                    # Quick overview
│   ├── SETUP_GUIDE.md              # Complete setup instructions
│   └── n8n-workflows/
│       ├── CONFIGURATION_GUIDE.md   # Workflow configuration
│       ├── configure_workflows.py   # Auto-config script
│       ├── workflow-1-search-notes.json
│       ├── workflow-2-read-note.json
│       ├── workflow-3-list-project-notes.json
│       ├── workflow-4-create-note.json
│       └── workflow-5-edit-note.json
│
├── README.md                        # You are here
├── CLAUDE.md                        # Claude Code context (optional)
├── LICENSE                          # MIT License
└── CHANGELOG.md                     # Version history
```

---

## 💡 Choosing Between Platforms

### Use Claude Code/Desktop if:
- You prefer working locally with VS Code or Claude Desktop
- You want offline support (once configured)
- You prefer keeping everything on your machine
- You're comfortable with Python and local configuration
- You want the fastest setup (~10 minutes)

### Use Claude.ai + n8n if:
- You want web-based workflows that run automatically
- You need scheduled task execution (e.g., daily summaries)
- You want to share workflows with team members
- You prefer a visual workflow builder
- You want Claude.ai's full capabilities

### Use Both if:
- You want maximum flexibility
- Different use cases need different approaches
- You like having options

**Good news:** Both use the same Notion data, so you can switch between them anytime!

---

## 🚀 Next Steps

1. **Choose your platform** (see table above)
2. **Open that platform's README:**
   - [Claude Code/Desktop](claude-code-desktop/README.md)
   - [Claude.ai + n8n](claude-ai/README.md)
3. **Follow the step-by-step guide**
4. **Verify everything works** (both guides include verification steps)
5. **Start using your skills!**

---

## 📋 How the Integrations Work

### Claude Code/Desktop Flow

```
You → Claude Code → Python Scripts → Notion API → Your Notion
                    (local)          (direct)      (data)
```

### Claude.ai + n8n Flow

```
You → Claude.ai → n8n Workflows → Python Scripts → Notion API → Your Notion
     (web)       (web-based)      (container)    (direct)      (data)
```

Both access the same Notion data using secure API authentication.

---

## 🔐 Security & Privacy

- **Your token stays on your machine** (Claude Code) or in n8n (Claude.ai)
- **No data sent to external services** except Notion's official API
- **Notion integration permissions** are limited to specific databases
- **Rate limiting** built in to respect API quotas
- **No tracking or analytics** in the integration code

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Open an issue describing what you'd like to improve
2. Fork the repository
3. Create a feature branch
4. Submit a pull request

Development guidelines:
- Follow the existing code structure
- Use `common.py` utilities for API calls
- Ensure all scripts output valid JSON
- Include comprehensive documentation
- Test with actual Notion data

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Thomas Frank** for creating [Ultimate Brain](https://thomasjfrank.com/brain/) - an excellent Notion template for productivity and knowledge management
- **Anthropic** for Claude and Claude Code
- **Notion** for their excellent API
- **n8n** for their incredible workflow automation platform

---

## 📞 Support

If you encounter issues:

1. **Check your platform's troubleshooting guide:**
   - [Claude Code Troubleshooting](claude-code-desktop/README.md#-troubleshooting)
   - [Claude.ai Troubleshooting](claude-ai/SETUP_GUIDE.md#part-5-troubleshooting)

2. **Run verification/validation:**
   - Claude Code: `python3 claude-code-desktop/validate_config.py`
   - Claude.ai: See workflow configuration section

3. **Check documentation:**
   - [Notion API Docs](https://developers.notion.com/)
   - [Claude Code Docs](https://code.claude.com/docs)
   - [n8n Docs](https://docs.n8n.io/)

4. **Open an issue** on GitHub with:
   - Description of the problem
   - Error messages (remove sensitive data!)
   - Which platform you're using
   - Steps to reproduce

---

**Ready to start?** Choose your platform above and follow the guide! 🚀

**Last updated:** 2024-12-06
