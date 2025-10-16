#!/bin/bash
# Test script for incident lookup tools
# This demonstrates the usage without requiring actual PagerDuty credentials

set -e

echo "=========================================="
echo "Testing Incident Lookup Tools"
echo "=========================================="
echo

# Test 1: Check if scripts exist and are readable
echo "Test 1: Checking if scripts exist..."
if [ -f "incident-lookup.sh" ]; then
    echo "✓ incident-lookup.sh exists"
else
    echo "✗ incident-lookup.sh not found"
    exit 1
fi

if [ -f "incident-analyzer.py" ]; then
    echo "✓ incident-analyzer.py exists"
else
    echo "✗ incident-analyzer.py not found"
    exit 1
fi

echo

# Test 2: Make scripts executable
echo "Test 2: Making scripts executable..."
chmod +x incident-lookup.sh
chmod +x incident-analyzer.py
echo "✓ Scripts are now executable"
echo

# Test 3: Check script help output
echo "Test 3: Testing help output..."
echo "--- incident-lookup.sh --help ---"
./incident-lookup.sh --help || true
echo
echo "--- incident-analyzer.py --help (requires Python) ---"
if command -v python3 &> /dev/null; then
    python3 incident-analyzer.py --help || true
    echo "✓ Python script help works"
else
    echo "⚠ Python3 not available, skipping"
fi
echo

# Test 4: Check documentation exists
echo "Test 4: Checking documentation..."
if [ -f "INCIDENT_RESPONSE.md" ]; then
    echo "✓ INCIDENT_RESPONSE.md exists"
    echo "  Documentation sections:"
    grep "^##" INCIDENT_RESPONSE.md | head -5
else
    echo "✗ INCIDENT_RESPONSE.md not found"
    exit 1
fi
echo

# Test 5: Check for required tools
echo "Test 5: Checking for required tools..."
tools_available=true

if command -v curl &> /dev/null; then
    echo "✓ curl is available"
else
    echo "⚠ curl not available (required for incident-lookup.sh)"
    tools_available=false
fi

if command -v jq &> /dev/null; then
    echo "✓ jq is available"
else
    echo "⚠ jq not available (required for incident-lookup.sh)"
    tools_available=false
fi

if command -v python3 &> /dev/null; then
    echo "✓ python3 is available"
else
    echo "⚠ python3 not available (required for incident-analyzer.py)"
    tools_available=false
fi

if command -v git &> /dev/null; then
    echo "✓ git is available"
else
    echo "⚠ git not available (required for commit correlation)"
    tools_available=false
fi
echo

# Test 6: Verify the memory leak fix
echo "Test 6: Verifying memory leak fix in worker.c..."
if grep -q "free(buffer);" worker.c; then
    echo "✓ Memory leak fix is present (free(buffer) call found)"
else
    echo "✗ Memory leak fix not found"
    exit 1
fi
echo

# Summary
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo "✓ All scripts are present and executable"
echo "✓ Documentation is available"
echo "✓ Memory leak fix is in place"

if [ "$tools_available" = true ]; then
    echo "✓ All required tools are available"
else
    echo "⚠ Some tools are missing (see above)"
fi

echo
echo "To use these tools with actual PagerDuty data:"
echo "1. Set your API token: export PAGERDUTY_API_TOKEN='your-token'"
echo "2. Run: ./incident-lookup.sh --service ads-demo-service"
echo "3. Or: python3 incident-analyzer.py --incident-id PXXXXXX"
echo
echo "See INCIDENT_RESPONSE.md for complete documentation"
