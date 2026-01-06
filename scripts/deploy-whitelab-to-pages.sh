#!/bin/bash
set -e

echo "======================================================"
echo "🥽 Deploying WhiteLab Reality Analyser to GitHub Pages"
echo "======================================================"

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Must run from repository root"
    exit 1
fi

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Build the 3D UI
echo ""
echo "🔨 Building WhiteLab 3D UI..."
npm run build

# Check if build succeeded
if [ ! -d "dist" ]; then
    echo "❌ Build failed - dist/ directory not found"
    exit 1
fi

# Backup old docs/ content (excluding .md files)
echo ""
echo "💾 Backing up old docs/ content..."
mkdir -p docs-backup
# More portable backup using tar
(cd docs && tar cf - --exclude='*.md' .) | (cd docs-backup && tar xf -) 2>/dev/null || true

# Clear old docs/ HTML/JS/CSS (keep .md documentation)
echo "🧹 Cleaning docs/ directory..."
rm -rf docs/*.html docs/*.js docs/*.css docs/assets/ docs/config.js

# Copy Vite build output to docs/
echo "📋 Copying build to docs/..."
cp -r dist/* docs/

# Create .nojekyll to disable Jekyll processing
touch docs/.nojekyll

echo ""
echo "======================================================"
echo "✅ WhiteLab build copied to docs/"
echo "======================================================"
echo ""
echo "Next steps:"
echo "1. Review changes: git status"
echo "2. Commit: git add docs/ && git commit -m '🥽 Deploy WhiteLab to GitHub Pages'"
echo "3. Push: git push origin main"
echo "4. Wait ~60s for GitHub Pages to update"
echo "5. Visit: https://harrie19.github.io/UMAJA-Core/"
echo ""
