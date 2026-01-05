#!/bin/bash
set -e

echo "======================================================"
echo "🥽 Setting up WhiteLab Reality Analyser"
echo "======================================================"
echo ""

# Check Python version
echo "📌 Checking Python version..."
python --version || python3 --version

# Check Node.js version
echo "📌 Checking Node.js version..."
node --version || echo "⚠️  Node.js not found. Please install Node.js v18+"

echo ""
echo "======================================================"
echo "📦 Installing Python dependencies..."
echo "======================================================"

# Install Python dependencies
pip install --upgrade pip
pip install Flask Flask-CORS flask-limiter gunicorn requests pytest
pip install torch sentence-transformers --extra-index-url https://download.pytorch.org/whl/cpu
pip install numpy pycountry pysrt Pillow cvxpy py_ecc lxml faiss-cpu prometheus-client scikit-learn
pip install streamlit opencv-python

echo ""
echo "======================================================"
echo "📦 Installing Node.js dependencies (Frontend)..."
echo "======================================================"

# Install frontend dependencies
if command -v npm &> /dev/null; then
    npm install
else
    echo "⚠️  npm not found. Skipping frontend dependencies."
    echo "   Please install Node.js and run 'npm install' manually."
fi

echo ""
echo "======================================================"
echo "📦 Installing Node.js dependencies (Backend/Server)..."
echo "======================================================"

# Install server dependencies
if command -v npm &> /dev/null; then
    cd server && npm install && cd ..
else
    echo "⚠️  npm not found. Skipping server dependencies."
fi

echo ""
echo "======================================================"
echo "📁 Creating directories..."
echo "======================================================"

# Create necessary directories
mkdir -p data/reality_checks
mkdir -p src/3d/scenes
mkdir -p src/3d/components
mkdir -p src/hooks
mkdir -p server

echo "✅ Directories created"

echo ""
echo "======================================================"
echo "🧪 Testing Reality Agent..."
echo "======================================================"

# Test reality check
python src/reality_agent.py

echo ""
echo "======================================================"
echo "✅ WhiteLab Reality Lab Setup Complete!"
echo "======================================================"
echo ""
echo "🚀 Start commands:"
echo ""
echo "  Terminal 1 - Backend WebSocket Server:"
echo "    cd server && node reality-stream.js"
echo ""
echo "  Terminal 2 - Frontend (3D UI):"
echo "    npm run dev"
echo ""
echo "  Terminal 3 - Streamlit Dashboard:"
echo "    streamlit run reality_dashboard.py"
echo ""
echo "======================================================"
echo "📖 Documentation: docs/REALITY_LAB_GUIDE.md"
echo "======================================================"
