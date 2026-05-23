#!/bin/bash
# Quick Start Script for Notion Clone

echo "🚀 Notion Clone - Quick Start"
echo "=============================="
echo ""

# Check Python
echo "✓ Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi
echo "✓ Python found: $(python3 --version)"

# Create virtual environment
echo ""
echo "✓ Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "✓ Activating virtual environment..."
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null

# Install dependencies
echo ""
echo "✓ Installing dependencies..."
pip install -q -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Create data directory
echo ""
echo "✓ Setting up data directory..."
mkdir -p data
echo "✓ Data directory ready"

# Run app
echo ""
echo "✓ Starting Notion Clone..."
echo ""
echo "🌐 App will open in your browser at: http://localhost:8501"
echo "📚 Press Ctrl+C to stop the server"
echo ""
streamlit run app.py