# Instructions for Claude Haiku 4.5

Hi Haiku! 👋

You have a detailed implementation plan to execute: `IMPLEMENTATION_PLAN.md`

## Your Mission

Restructure this repository to make it production-ready and user-friendly for two audiences:
1. Claude Code/Desktop users (local installation)
2. Claude.ai + n8n users (web-based workflows)

## What to Do

1. **Read the plan:** Open and read `IMPLEMENTATION_PLAN.md` carefully
2. **Follow the phases:** Execute Phase 1 through Phase 8 in order
3. **Test as you go:** Validate JSON syntax, check file paths, ensure scripts work
4. **Commit at the end:** Create one comprehensive commit (instructions in Phase 8)
5. **Do NOT push:** The user will manually push to GitHub

## Key Requirements

✅ **DO:**
- Follow the implementation plan phases in order
- Create all specified files with the content structures outlined
- Update existing files as specified
- Test scripts for syntax errors
- Validate JSON files
- Use clear, consistent documentation style
- Create helpful error messages
- Add placeholder systems for database IDs

❌ **DON'T:**
- Push to GitHub (user will do this)
- Include any real database IDs or tokens
- Commit the Archive/ folder
- Commit the .claude/ folder
- Skip any phases
- Deviate significantly from the plan without good reason

## Important Files to Check

Before committing, verify:
- `.gitignore` excludes `Archive/` and `.claude/`
- No sensitive data in any files
- All JSON files are valid JSON
- All Python scripts have correct syntax
- All markdown links work
- File paths are accurate

## At the End

Print a summary with:
- ✅ Files created (count)
- ✅ Files modified (count)
- ✅ Files deleted (count)
- ✅ Commit message preview
- ✅ Verification: "Archive/ not in commit: YES/NO"
- ✅ Next steps for user

## Need Clarification?

The plan is comprehensive, but if something is genuinely unclear:
1. Make a reasonable decision following the plan's spirit
2. Document your decision in comments
3. Note it in your final summary

Good luck! The plan is detailed and thorough - you've got this! 🚀
