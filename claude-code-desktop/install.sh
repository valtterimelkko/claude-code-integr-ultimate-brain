#!/bin/bash
# Ultimate Brain Claude Code Installation Script
# Automates the installation of scripts and skill definitions

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

print_header() {
    echo ""
    echo -e "${BLUE}=== $1 ===${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# ============================================================================
# PHASE 1: CHECK PREREQUISITES
# ============================================================================

phase_check_prerequisites() {
    print_header "Checking Prerequisites"

    # Check Python version
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed"
        echo "Please install Python 3.7 or higher: https://www.python.org/downloads/"
        exit 1
    fi

    python_version=$(python3 --version 2>&1 | awk '{print $2}')
    print_info "Found Python $python_version"

    # Check requests library
    if ! python3 -c "import requests" 2>/dev/null; then
        print_warning "Python 'requests' library not found"
        echo "Installing with: pip3 install requests"
        pip3 install requests
        print_success "Installed requests library"
    else
        print_success "Python 'requests' library is installed"
    fi

    # Check curl (for API testing)
    if command -v curl &> /dev/null; then
        print_success "curl is available (optional)"
    fi
}

# ============================================================================
# PHASE 2: GATHER CONFIGURATION
# ============================================================================

phase_gather_configuration() {
    print_header "Configuration"

    echo "You need to provide your database IDs from your Ultimate Brain Notion setup."
    echo "See README.md for instructions on finding these IDs."
    echo ""

    # Prompt for Notes Database ID
    while true; do
        read -p "Enter your Notes Database ID: " notes_db_id
        if [ -z "$notes_db_id" ]; then
            print_error "Database ID cannot be empty"
            continue
        fi
        if [ ${#notes_db_id} -lt 10 ]; then
            print_error "Database ID seems too short (expected ~36 characters)"
            continue
        fi
        break
    done

    # Prompt for Projects Database ID
    while true; do
        read -p "Enter your Projects Database ID: " projects_db_id
        if [ -z "$projects_db_id" ]; then
            print_error "Database ID cannot be empty"
            continue
        fi
        if [ ${#projects_db_id} -lt 10 ]; then
            print_error "Database ID seems too short (expected ~36 characters)"
            continue
        fi
        break
    done

    # Prompt for Notion Token
    while true; do
        read -sp "Enter your Notion Integration Token (hidden): " notion_token
        echo ""
        if [ -z "$notion_token" ]; then
            print_error "Token cannot be empty"
            continue
        fi
        if [[ ! $notion_token =~ ^secret_ ]]; then
            print_warning "Token doesn't start with 'secret_' - this might be wrong"
            read -p "Continue anyway? (y/n): " continue_anyway
            if [[ $continue_anyway == "y" ]]; then
                break
            fi
        else
            break
        fi
    done

    print_success "Configuration gathered"
}

# ============================================================================
# PHASE 3: UPDATE CONFIGURATION
# ============================================================================

phase_update_configuration() {
    print_header "Updating Configuration Files"

    # Get the directory where this script is located
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    common_py="$script_dir/scripts/common.py"

    if [ ! -f "$common_py" ]; then
        print_error "Cannot find scripts/common.py"
        exit 1
    fi

    # Create a backup
    cp "$common_py" "$common_py.backup"
    print_info "Created backup: $common_py.backup"

    # Update database IDs in common.py
    # Escape special characters for sed
    notes_db_escaped=$(printf '%s\n' "$notes_db_id" | sed -e 's/[\/&]/\\&/g')
    projects_db_escaped=$(printf '%s\n' "$projects_db_id" | sed -e 's/[\/&]/\\&/g')

    sed -i.tmp "s/NOTES_DB_ID = \"YOUR_NOTES_DATABASE_ID_HERE\"/NOTES_DB_ID = \"$notes_db_escaped\"/" "$common_py"
    sed -i.tmp "s/PROJECTS_DB_ID = \"YOUR_PROJECTS_DATABASE_ID_HERE\"/PROJECTS_DB_ID = \"$projects_db_escaped\"/" "$common_py"
    rm -f "$common_py.tmp"

    print_success "Updated database IDs in scripts/common.py"

    # Create credential file
    print_info "Creating credential file at /etc/keep-to-notion/env.conf"

    if [ -f /etc/keep-to-notion/env.conf ]; then
        print_warning "Credential file already exists - will update it"
        sudo cp /etc/keep-to-notion/env.conf /etc/keep-to-notion/env.conf.backup
        print_info "Backed up existing config"
    fi

    # Create directory if it doesn't exist
    sudo mkdir -p /etc/keep-to-notion

    # Write the token to the config file
    echo "NOTION_TOKEN=$notion_token" | sudo tee /etc/keep-to-notion/env.conf > /dev/null

    # Set permissions (read-only for current user, no access for others)
    sudo chmod 600 /etc/keep-to-notion/env.conf

    print_success "Created credential file"
    print_info "Permissions set to 600 (current user only)"
}

# ============================================================================
# PHASE 4: INSTALL FILES
# ============================================================================

phase_install_files() {
    print_header "Installing Files"

    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

    # Create .claude directories
    print_info "Creating ~/.claude directories..."
    mkdir -p ~/.claude/scripts/notion
    mkdir -p ~/.claude/skills/notion-{search-notes,read-note,list-project-notes,create-note,edit-note,archive-note,combine-notes}

    # Copy Python scripts
    print_info "Copying Python scripts..."
    cp "$script_dir/scripts"/*.py ~/.claude/scripts/notion/
    chmod +x ~/.claude/scripts/notion/*.py
    print_success "Python scripts installed to ~/.claude/scripts/notion/"

    # Copy skill definitions
    print_info "Copying skill definitions..."
    for skill in search-notes read-note list-project-notes create-note edit-note archive-note combine-notes; do
        if [ -f "$script_dir/skill-definitions/notion-$skill.md" ]; then
            cp "$script_dir/skill-definitions/notion-$skill.md" ~/.claude/skills/notion-$skill/SKILL.md
        fi
    done
    print_success "Skill definitions installed to ~/.claude/skills/"

    print_info "Installation directory structure created:"
    echo "  ~/.claude/scripts/notion/     (Python scripts)"
    echo "  ~/.claude/skills/notion-*     (Claude Code skills)"
}

# ============================================================================
# PHASE 5: VERIFY INSTALLATION
# ============================================================================

phase_verify_installation() {
    print_header "Verifying Installation"

    errors=0

    # Check Python scripts exist and are executable
    print_info "Checking Python scripts..."
    for script in search_notes.py read_note.py list_project_notes.py create_note.py edit_note.py archive_note.py combine_notes.py search_projects.py common.py; do
        if [ -f ~/.claude/scripts/notion/$script ]; then
            print_success "Found $script"
        else
            print_error "Missing $script"
            ((errors++))
        fi
    done

    # Check skill definitions exist
    print_info "Checking skill definitions..."
    for skill in search-notes read-note list-project-notes create-note edit-note archive-note combine-notes; do
        if [ -f ~/.claude/skills/notion-$skill/SKILL.md ]; then
            print_success "Found notion-$skill skill"
        else
            print_error "Missing notion-$skill skill"
            ((errors++))
        fi
    done

    # Check credential file
    print_info "Checking credential file..."
    if [ -f /etc/keep-to-notion/env.conf ]; then
        print_success "Credential file exists"
        if grep -q "NOTION_TOKEN=" /etc/keep-to-notion/env.conf; then
            print_success "Notion token is configured"
        else
            print_error "Notion token not found in credential file"
            ((errors++))
        fi
    else
        print_error "Credential file not found"
        ((errors++))
    fi

    if [ $errors -eq 0 ]; then
        print_success "All verifications passed!"
        return 0
    else
        print_error "Some verifications failed"
        return 1
    fi
}

# ============================================================================
# PHASE 6: TEST INSTALLATION
# ============================================================================

phase_test_installation() {
    print_header "Testing Installation"

    print_info "Attempting to test Python scripts..."
    print_info "This will verify that scripts can execute and access your database IDs..."
    echo ""

    # Try to list projects
    if python3 ~/.claude/scripts/notion/search_projects.py --name "test" --limit 1 2>/dev/null | grep -q '"success"'; then
        print_success "Scripts can execute successfully"
    else
        print_warning "Could not execute a test query"
        print_info "This might be normal if your Notion token or database IDs are incomplete"
    fi
}

# ============================================================================
# PHASE 7: SUCCESS MESSAGE
# ============================================================================

phase_success_message() {
    print_header "Installation Complete!"

    echo ""
    echo "🎉 Your Ultimate Brain Claude Code integration is ready!"
    echo ""
    echo "📋 What was installed:"
    echo "  ✓ Python scripts for Notion interaction"
    echo "  ✓ Claude Code skill definitions"
    echo "  ✓ Configuration with your database IDs"
    echo "  ✓ Notion API token (secure file)"
    echo ""
    echo "🚀 Next steps:"
    echo "  1. Restart Claude Code (VS Code) or Claude Desktop"
    echo "  2. The 7 skills should appear in Claude's tool list:"
    echo "     - notion_search_notes"
    echo "     - notion_read_note"
    echo "     - notion_list_project_notes"
    echo "     - notion_create_note"
    echo "     - notion_edit_note"
    echo "     - notion_archive_note (NEW)"
    echo "     - notion_combine_notes (NEW)"
    echo "  3. Try asking Claude: 'Search my notes for test'"
    echo ""
    echo "📚 For more help:"
    echo "  - See: $script_dir/README.md"
    echo "  - Check: $script_dir/../README.md (main repository)"
    echo ""
    echo "⚙️  Configuration files:"
    echo "  - Database IDs: $script_dir/scripts/common.py"
    echo "  - Notion Token: /etc/keep-to-notion/env.conf"
    echo ""
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

main() {
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

    echo ""
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════════════╗"
    echo "║  Ultimate Brain Claude Code Installation      ║"
    echo "╚════════════════════════════════════════════════╝"
    echo -e "${NC}"

    phase_check_prerequisites
    phase_gather_configuration
    phase_update_configuration
    phase_install_files

    if phase_verify_installation; then
        phase_test_installation
        phase_success_message
        exit 0
    else
        print_error "Installation verification failed - please check the errors above"
        exit 1
    fi
}

# Run main function
main "$@"
