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

    # Check requests library without modifying the user's Python installation.
    if ! python3 -c "import requests" 2>/dev/null; then
        print_error "Python 'requests' library is not installed"
        echo "Install it in your chosen environment with: python3 -m pip install requests"
        exit 1
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

    # Keep credentials and database IDs outside the repository and source copies.
    config_home="${XDG_CONFIG_HOME:-$HOME/.config}"
    config_dir="$config_home/ultimate-brain-notion"
    notion_config_file="$config_dir/env.conf"
    mkdir -p "$config_dir"
    umask 077

    cat > "$notion_config_file" <<EOF
NOTES_DB_ID=$notes_db_id
PROJECTS_DB_ID=$projects_db_id
NOTION_TOKEN=$notion_token
EOF
    chmod 600 "$notion_config_file"
    export NOTION_CONFIG_FILE="$notion_config_file"

    print_success "Created user-local configuration at $notion_config_file"
    print_info "The repository and installed Python scripts were not modified"
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

    # Check user-local credential file
    config_home="${XDG_CONFIG_HOME:-$HOME/.config}"
    notion_config_file="${NOTION_CONFIG_FILE:-$config_home/ultimate-brain-notion/env.conf}"
    print_info "Checking credential file..."
    if [ -f "$notion_config_file" ]; then
        print_success "Credential file exists"
        if grep -q "^NOTION_TOKEN=" "$notion_config_file"; then
            print_success "Notion token is configured"
        else
            print_error "Notion token not found in credential file"
            ((errors++))
        fi
    else
        print_error "Credential file not found: $notion_config_file"
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

    # Import configuration and script dependencies only; do not contact Notion.
    if NOTION_CONFIG_FILE="${NOTION_CONFIG_FILE:-${XDG_CONFIG_HOME:-$HOME/.config}/ultimate-brain-notion/env.conf}" \
        PYTHONPATH="$HOME/.claude/scripts/notion" \
        python3 -c "import common; assert common.NOTES_DB_ID and common.PROJECTS_DB_ID"; then
        print_success "Scripts can import configuration successfully"
    else
        print_error "Installed scripts could not load configuration"
        return 1
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
    echo "  ✓ User-local configuration with database IDs"
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
    echo "  - Database IDs and token: ${NOTION_CONFIG_FILE:-${XDG_CONFIG_HOME:-$HOME/.config}/ultimate-brain-notion/env.conf}"
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
