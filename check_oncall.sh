#!/bin/bash
# Wrapper script to check who's on call for PD Advance Team

set -e

# Default team name
TEAM_NAME="PD Advance Team"

# Allow override via command line argument
if [ $# -gt 0 ]; then
    TEAM_NAME="$*"
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is required but not installed" >&2
    exit 1
fi

# Run the Python script
python3 "$(dirname "$0")/check_oncall.py" "$TEAM_NAME"
