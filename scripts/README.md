# cws-helpers Scripts

This directory contains utility scripts for maintaining and releasing the cws-helpers package.

## Available Scripts

### Release Scripts

#### release.sh

A basic script to push version updates for the cws-helpers package.

```bash
./scripts/release.sh <version> "<commit_message>"
```

Example:
```bash
./scripts/release.sh 0.11.0 "Add new feature X and fix bug Y"
```

This script will:
1. Update version in src/cws_helpers/__init__.py
2. Update version in pyproject.toml
3. Commit the changes
4. Create a version tag
5. Push changes and tag to GitHub

**Note:** You should update the CHANGELOG.md manually *before* running this script.
