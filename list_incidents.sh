#!/bin/bash
# Wrapper script to list PagerDuty incidents

# Check if PAGERDUTY_API_TOKEN is set
if [ -z "$PAGERDUTY_API_TOKEN" ]; then
    echo "Error: PAGERDUTY_API_TOKEN environment variable is not set"
    echo "Please set it with: export PAGERDUTY_API_TOKEN=your_token_here"
    exit 1
fi

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed"
    exit 1
fi

# Check if requests library is installed
if ! python3 -c "import requests" 2>/dev/null; then
    echo "Installing required dependencies..."
    pip install -r requirements.txt
fi

# Run the script
python3 list_incidents.py "$@"
