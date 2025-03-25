#!/bin/bash

# release.sh - Push version updates for cws-helpers
# 
# Usage: ./scripts/release.sh <version> "<commit_message>"
# Example: ./scripts/release.sh 0.11.0 "Add new feature X and fix bug Y"
#
# This script will:
# 1. Update version in src/cws_helpers/__init__.py
# 2. Update version in pyproject.toml
# 3. Commit the changes
# 4. Create a version tag
# 5. Push changes and tag to GitHub
#
# Note: CHANGELOG.md should be updated before running this script.

set -e  # Exit immediately if a command exits with a non-zero status

# Check if the correct number of arguments is provided
if [ $# -lt 2 ]; then
    echo "Usage: $0 <version> \"<commit_message>\""
    echo "Example: $0 0.11.0 \"Add new feature X and fix bug Y\""
    exit 1
fi

VERSION=$1
COMMIT_MESSAGE=$2
TAG_NAME="v$VERSION"

echo "Starting release process for version $VERSION"
echo "Commit message: $COMMIT_MESSAGE"
echo "Note: Make sure CHANGELOG.md has already been updated for this version."
echo "Continue? (y/n)"
read continue_release
if [ "$continue_release" != "y" ] && [ "$continue_release" != "Y" ]; then
    echo "Release aborted."
    exit 1
fi

# Update version in __init__.py
echo "Updating version in src/cws_helpers/__init__.py"
sed -i "" "s/__version__ = \"[0-9.]*\"/__version__ = \"$VERSION\"/" src/cws_helpers/__init__.py

# Update version in pyproject.toml
echo "Updating version in pyproject.toml"
sed -i "" "s/version = \"[0-9.]*\"/version = \"$VERSION\"/" pyproject.toml

# Check if there are any changes to commit
if git diff --quiet src/cws_helpers/__init__.py pyproject.toml; then
    echo "No changes detected. Please make sure you've entered a new version number."
    exit 1
fi

# Commit changes
echo "Committing changes"
git add src/cws_helpers/__init__.py pyproject.toml
git commit -m "chore: Bump version to $VERSION" -m "$COMMIT_MESSAGE"

# Create tag
echo "Creating tag $TAG_NAME"
git tag -a "$TAG_NAME" -m "Version $VERSION - $COMMIT_MESSAGE"

# Push changes and tag
echo "Pushing changes and tag to GitHub"
git push origin main
git push origin "$TAG_NAME"

echo "Release process completed successfully!"
echo "Don't forget to create a release on GitHub:"
echo "https://github.com/caseywschmid/cws-helpers/releases/new?tag=$TAG_NAME" 