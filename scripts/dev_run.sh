#!/bin/bash
# Development runner with automatic cache prevention

echo "🚀 Starting Focus Backdrop in development mode (preventing cache files)..."

# Clean any existing cache files
find . \( -name "*.pyc" -o -name "__pycache__" \) -exec rm -rf {} + 2>/dev/null

# Run with cache prevention
python3 -B -m focus_backdrop "$@"
