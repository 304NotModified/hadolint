# Hadolint Wiki Pages

This directory contains automatically generated wiki pages for all Hadolint rules.

## Contents

- **Home.md**: The main wiki landing page with an index of all rules
- **DL*.md**: Individual pages for each rule (66 rules total)

## How to Upload to GitHub Wiki

Since GitHub wikis are stored in a separate Git repository, follow these steps to upload these pages:

### Option 1: Using Git

1. Clone the wiki repository:
   ```bash
   git clone https://github.com/hadolint/hadolint.wiki.git
   ```

2. Copy all `.md` files from this directory to the wiki repository:
   ```bash
   cp wiki/*.md hadolint.wiki/
   ```

3. Commit and push the changes:
   ```bash
   cd hadolint.wiki
   git add *.md
   git commit -m "Add auto-generated rule documentation pages"
   git push origin master
   ```

### Option 2: Using GitHub Web Interface

1. Go to the [Hadolint Wiki](https://github.com/hadolint/hadolint/wiki)
2. Click "New Page" for each rule
3. Copy the content from the corresponding `.md` file in this directory
4. Save the page

### Option 3: Using a Script

We provide a helper script to automate the upload process:

```bash
# From the hadolint repository root
./scripts/upload_wiki.sh
```

## Maintenance

These wiki pages are generated from the Haskell source files in `src/Hadolint/Rule/`.

To regenerate the wiki pages after rule changes:

```bash
python3 scripts/generate_wiki.py
```

## Structure of Each Rule Page

Each rule page includes:

- **Severity**: Error, Warning, Info, or Style
- **Description**: What the rule checks for
- **Rationale**: Why this rule exists
- **Examples**: Bad and good code examples
- **Configuration**: How to ignore the rule if needed
- **See Also**: Links to related documentation

## Notes

- The wiki repository is separate from the main Hadolint repository
- Wiki pages use GitHub Flavored Markdown
- Internal wiki links use the format `[RuleCode](RuleCode)` (e.g., `[DL3000](DL3000)`)
- These files can also be used as standalone documentation

## License

These documentation files are part of the Hadolint project and are licensed under GPL-3.0.
