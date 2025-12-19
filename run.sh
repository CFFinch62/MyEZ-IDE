#!/bin/bash
# Run script for EZ IDE

# Change to script directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup first..."
    echo ""
    ./setup.sh
fi

# Activate and run
source venv/bin/activate
python3 main.py "$@"
