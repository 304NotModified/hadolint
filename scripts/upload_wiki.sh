#!/bin/bash
# Script to upload wiki pages to the GitHub wiki repository

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
WIKI_DIR="$REPO_ROOT/wiki"
TEMP_WIKI_CLONE="/tmp/hadolint.wiki"

echo -e "${GREEN}Hadolint Wiki Upload Script${NC}"
echo "=================================="
echo ""

# Check if wiki directory exists
if [ ! -d "$WIKI_DIR" ]; then
    echo -e "${RED}Error: wiki directory not found at $WIKI_DIR${NC}"
    echo "Please run 'python3 scripts/generate_wiki.py' first to generate wiki pages."
    exit 1
fi

# Count wiki pages
PAGE_COUNT=$(find "$WIKI_DIR" -name "*.md" | wc -l)
echo -e "${GREEN}Found $PAGE_COUNT wiki pages to upload${NC}"
echo ""

# Prompt for confirmation
echo -e "${YELLOW}This will clone the wiki repository and upload all wiki pages.${NC}"
read -p "Do you want to continue? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Upload cancelled."
    exit 0
fi

# Clean up any existing clone
if [ -d "$TEMP_WIKI_CLONE" ]; then
    echo "Cleaning up existing wiki clone..."
    rm -rf "$TEMP_WIKI_CLONE"
fi

# Clone the wiki repository
echo "Cloning wiki repository..."
if ! git clone https://github.com/hadolint/hadolint.wiki.git "$TEMP_WIKI_CLONE"; then
    echo -e "${RED}Error: Failed to clone wiki repository${NC}"
    echo "Make sure you have access to the repository and the wiki is enabled."
    exit 1
fi

# Copy wiki pages
echo "Copying wiki pages..."
cp -v "$WIKI_DIR"/*.md "$TEMP_WIKI_CLONE/"

# Change to wiki directory
cd "$TEMP_WIKI_CLONE"

# Check if there are changes
if git diff --quiet && git diff --cached --quiet; then
    echo -e "${YELLOW}No changes detected in wiki pages.${NC}"
    echo "Wiki is already up to date."
    rm -rf "$TEMP_WIKI_CLONE"
    exit 0
fi

# Show changes
echo ""
echo "Changes to be committed:"
git status --short

# Commit changes
echo ""
echo "Committing changes..."
git add *.md
git commit -m "Update auto-generated rule documentation

- Updated wiki pages for all Hadolint rules
- Generated from source code on $(date +%Y-%m-%d)
- Total pages: $PAGE_COUNT"

# Push changes
echo ""
echo "Pushing changes to GitHub wiki..."
if git push origin master; then
    echo -e "${GREEN}✓ Successfully uploaded wiki pages!${NC}"
    echo ""
    echo "View the wiki at: https://github.com/hadolint/hadolint/wiki"
else
    echo -e "${RED}Error: Failed to push changes${NC}"
    echo "The changes are committed locally at: $TEMP_WIKI_CLONE"
    echo "You may need to push manually or check your permissions."
    exit 1
fi

# Clean up
echo ""
echo "Cleaning up..."
cd "$REPO_ROOT"
rm -rf "$TEMP_WIKI_CLONE"

echo -e "${GREEN}✓ Done!${NC}"
