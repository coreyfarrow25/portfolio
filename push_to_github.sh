#!/bin/bash
# ================================================================
# Portfolio → GitHub Push Script
# Run this from Terminal inside the portfolio folder
# ================================================================

set -e

REPO_NAME="portfolio"
GITHUB_USERNAME="${1:-YOUR_GITHUB_USERNAME}"

if [ "$GITHUB_USERNAME" = "YOUR_GITHUB_USERNAME" ]; then
  echo "Usage: bash push_to_github.sh YOUR_GITHUB_USERNAME"
  echo "Example: bash push_to_github.sh coreyfarrowjr"
  exit 1
fi

echo ""
echo "=================================================="
echo "  Setting up portfolio repo for: $GITHUB_USERNAME"
echo "=================================================="
echo ""

# Move into the portfolio directory (in case script is run from parent)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Remove any leftover .git from a failed attempt
if [ -d ".git" ]; then
  echo "Removing existing .git folder..."
  rm -rf .git
fi

# Init fresh repo
git init
git config user.email "coreyfarrow25@gmail.com"
git config user.name "Corey Farrow"
git branch -M main

# Stage everything
git add .

# Commit
git commit -m "Initial commit: Data & Product Portfolio

- beats-by-dre-analytics: EDA, sentiment, correlation on 5,127 Amazon reviews
- bereal-pm-externship: RICE scoring, PRD-Lite, user testing, pitch
- intro-stat-with-r: R scripts for data merging and descriptive statistics
- intro-to-statistical-analysis: Python/Jupyter for regression, probability, hypothesis testing"

echo ""
echo "✅ Local commit done."
echo ""
echo "Next: create the repo on GitHub and push."
echo "Creating repo via GitHub CLI (gh)..."
echo ""

# Try gh CLI first (if installed)
if command -v gh &> /dev/null; then
  gh repo create "$REPO_NAME" \
    --public \
    --description "Data analytics and product management portfolio — Python, R, NLP, Pandas, TextBlob, Matplotlib" \
    --push \
    --source .
  echo ""
  echo "=================================================="
  echo "  ✅ Done! Repo live at:"
  echo "  https://github.com/$GITHUB_USERNAME/$REPO_NAME"
  echo "=================================================="
else
  # gh not installed — manual push
  git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
  echo "gh CLI not found. Do this manually:"
  echo ""
  echo "  1. Go to https://github.com/new"
  echo "  2. Name: $REPO_NAME"
  echo "  3. Set to Public, NO readme/gitignore"
  echo "  4. Click Create repository"
  echo "  5. Then run:"
  echo ""
  echo "     git push -u origin main"
  echo ""
  echo "  Repo will be at: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
fi
