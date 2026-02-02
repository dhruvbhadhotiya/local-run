#!/bin/bash
# Campus AI Chat Platform - Linux/Mac Start Script

echo "Starting Campus AI Chat Platform..."
echo

# Check if virtual environment exists
if [ ! -d ".env" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run: python setup.py"
    exit 1
fi

# Activate virtual environment
source .env/bin/activate

# Check if model exists
if ! ls models/*.gguf 1> /dev/null 2>&1; then
    echo "WARNING: No model found in models/ directory"
    echo "Please run: python scripts/download_model.py"
    exit 1
fi

# Start server
echo
echo "Server starting at http://localhost:8080"
echo "Press Ctrl+C to stop the server"
echo

python server.py

# Deactivate on exit
deactivate
