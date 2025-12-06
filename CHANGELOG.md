# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-12-06

### Added

#### Claude.ai + n8n Integration
- Complete web-based integration with Claude.ai using n8n workflows
- 5 pre-built n8n workflow JSON templates (search, read, list, create, edit)
- Automated workflow configuration script (`configure_workflows.py`)
- Comprehensive setup guide (`claude-ai/SETUP_GUIDE.md`) with 4 phases
- Workflow configuration guide with manual and automatic options
- Support for both self-hosted and cloud-based n8n instances
- Docker setup instructions with custom Dockerfile for n8n

#### Claude Code/Desktop Improvements
- Automated installation script (`install.sh`) for quick setup
- Configuration validation tool (`validate_config.py`)
- Enhanced README with multiple installation options
- Better troubleshooting documentation
- Testing commands and verification procedures
- Installation time reduced to ~10 minutes (from ~30)

#### Repository Improvements
- Completely restructured README for dual-platform support
- Clear decision tree for users to choose their platform
- Platform-specific installation guides
- Updated repository structure documentation
- Security and privacy information
- Contributing guidelines

### Changed

#### Documentation Restructure
- Main README now focuses on platform selection and quick start
- Moved detailed Claude Code installation to `claude-code-desktop/README.md`
- Merged two separate n8n guides into single comprehensive `claude-ai/SETUP_GUIDE.md`
- Improved consistency across all documentation
- Better visual hierarchy with emoji indicators and tables

#### File Organization
- `claude-ai/` now contains both setup guide and workflow files
- `claude-code-desktop/` now includes installation tools
- Clearer separation of concerns between platforms
- All platform-specific documentation in their respective folders

#### Installation Process
- Added automated setup with `install.sh` script
- User-friendly prompts for database IDs and tokens
- Automatic file copying and permission setting
- Comprehensive verification and testing

### Fixed

- Clarified database ID formatting requirements
- Improved error messages with actionable solutions
- Better permission handling in installation scripts
- Fixed inconsistent documentation across guides
- Corrected broken internal links

### Removed

- Duplicate n8n documentation (merged into single guide)
- Outdated installation instructions
- Redundant configuration steps

### Documentation

- Added detailed troubleshooting sections for both platforms
- Platform-specific FAQ coverage
- Security best practices documented
- Architecture diagrams and visual flows
- Example use cases and command samples

## [1.0.0] - 2024-12-05

### Added

#### Initial Release
- 5 Claude Code skills for Ultimate Brain integration
- Python script backend for Notion API interaction
- Support for Claude Code (VS Code extension)
- Support for Claude Desktop (native application)
- Comprehensive documentation

#### Core Functionality
- `notion_search_notes` - Search notes by keyword
- `notion_read_note` - Read full note content
- `notion_list_project_notes` - List notes in a project
- `notion_create_note` - Create new notes in Inbox
- `notion_edit_note` - Edit/append note content

#### Backend Scripts
- `common.py` - Shared utilities and Notion API configuration
- `search_notes.py` - Note searching functionality
- `read_note.py` - Note reading functionality
- `list_project_notes.py` - Project note listing
- `create_note.py` - Note creation
- `edit_note.py` - Note editing
- `search_projects.py` - Project finding

#### Documentation
- Installation guide with 8 detailed steps
- Architecture overview
- Troubleshooting section
- Usage examples
- Contributing guidelines

#### Features
- Structured JSON output from all operations
- Automatic archived item filtering
- Partial name matching for projects/notes
- Rate limit compliance with 0.3s delays
- Clear, actionable error messages
- Context-efficient data returns

## Version Numbering

- **Major (X.y.z)**: Breaking changes, new platforms, major restructuring
- **Minor (x.Y.z)**: New features, new platforms support
- **Patch (x.y.Z)**: Bug fixes, documentation, small improvements

---

## Roadmap

### Planned for Future Releases

- Support for additional Ultimate Brain components (Tasks, Areas, Resources)
- Webhook support for automated integrations
- Advanced filtering and search capabilities
- Performance optimizations
- Additional Claude Code skill examples
- Integration with other AI platforms
- Mobile-friendly documentation

### Under Consideration

- Browser extension for direct Notion access
- Advanced scheduling for Claude.ai workflows
- Custom workflow templates
- Analytics and usage tracking (privacy-focused)
- Team collaboration features
- Multi-workspace support

---

## Migration Guide

### From v1.0.0 to v2.0.0

#### If using Claude Code/Desktop

1. **No migration needed!** Your existing installation continues to work
2. **Optionally upgrade to new installation script:**
   ```bash
   cd claude-code-desktop
   chmod +x install.sh
   ./install.sh
   ```
3. Run validation to ensure everything is configured:
   ```bash
   python3 validate_config.py
   ```

#### If interested in Claude.ai + n8n

1. Follow the new Claude.ai setup guide: `claude-ai/SETUP_GUIDE.md`
2. Configure workflows using the new configuration script
3. Both platforms can coexist and access the same Notion data

#### Documentation Changes

- Check the new main `README.md` for updated navigation
- Platform-specific guides are now in their respective folders
- Old guides have been consolidated (no information lost)

---

## Support

For questions about any version:
- Check the README in your chosen platform folder
- Review the troubleshooting section in that platform's guide
- Open an issue on GitHub with details

---

**Last updated:** 2024-12-06
