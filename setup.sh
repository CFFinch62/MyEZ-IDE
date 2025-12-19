#!/bin/bash
# Setup script for EZ IDE

set -e

echo "================================"
echo "   EZ IDE Setup"
echo "================================"
echo ""

# Check Python version
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "Error: Python 3 is required but not found."
    echo "Please install Python 3.8 or higher."
    exit 1
fi

# Verify Python version is 3.8+
PY_VERSION=$($PYTHON_CMD -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
PY_MAJOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info.major)')
PY_MINOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info.minor)')

if [ "$PY_MAJOR" -lt 3 ] || ([ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 8 ]); then
    echo "Error: Python 3.8+ is required. Found Python $PY_VERSION"
    exit 1
fi

echo "✓ Found Python $PY_VERSION"

# Change to script directory
cd "$(dirname "$0")"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip -q

# Install PyQt6
echo ""
echo "Installing dependencies..."
pip install PyQt6>=6.5.0 -q
echo "✓ Dependencies installed"

echo ""
echo "================================"
echo "   Setup Complete!"
echo "================================"
echo ""
echo "To run EZ IDE:"
echo "  ./run.sh"
echo ""
echo "Or manually:"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
