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
    yarn install
fi

# Build the 3D UI
echo ""
echo "🔨 Building WhiteLab 3D UI..."
VITE_BACKEND_URL=https://web-production-016d1.up.railway.app \
VITE_REALITY_STREAM_URL=https://web-production-016d1.up.railway.app \
yarn build

# Check if build succeeded
if [ ! -d "dist" ]; then
    echo "❌ Build failed - dist/ directory not found"
    exit 1
fi

# Preserve markdown files
echo ""
echo "💾 Preserving markdown files..."
mkdir -p /tmp/docs-backup
find docs/ -name "*.md" -exec cp {} /tmp/docs-backup/ \; 2>/dev/null || true

# Clear old docs/ HTML/JS/CSS (keep .md documentation)
echo "🧹 Cleaning docs/ directory..."
rm -rf docs/*.html docs/*.js docs/*.css docs/assets/

# Copy Vite build output to docs/
echo "📋 Copying build to docs/..."
cp -r dist/* docs/

# Restore markdown files
cp /tmp/docs-backup/*.md docs/ 2>/dev/null || true

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
echo "3. Push: git push"
echo "4. Wait ~60s for GitHub Pages to update"
echo "5. Visit: https://harrie19.github.io/UMAJA-Core/"
echo ""
