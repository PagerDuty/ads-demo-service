#!/bin/bash
# Verification script for PagerDuty MCP integration

set -e

echo "==================================="
echo "PagerDuty MCP Integration Verification"
echo "==================================="
echo ""

# Check if agent configuration exists
echo "✓ Checking agent configuration file..."
if [ -f ".github/agents/my-agent.md" ]; then
    echo "  ✓ Agent configuration found"
else
    echo "  ✗ Agent configuration NOT found"
    exit 1
fi

# Check agent name
echo "✓ Checking agent name..."
if grep -q "name: pagerduty-incident-responder" ".github/agents/my-agent.md"; then
    echo "  ✓ Agent name: pagerduty-incident-responder"
else
    echo "  ✗ Agent name not found or incorrect"
    exit 1
fi

# Check MCP server configuration
echo "✓ Checking MCP server configuration..."
if grep -q "pagerduty-mcp:" ".github/agents/my-agent.md"; then
    echo "  ✓ MCP server configured"
else
    echo "  ✗ MCP server configuration NOT found"
    exit 1
fi

# Check MCP server URL
echo "✓ Checking MCP server URL..."
if grep -q "url: 'https://mcp.pagerduty.com/mcp'" ".github/agents/my-agent.md"; then
    echo "  ✓ MCP URL: https://mcp.pagerduty.com/mcp"
else
    echo "  ✗ MCP URL not found or incorrect"
    exit 1
fi

# Check required MCP tools
echo "✓ Checking required MCP tools..."
REQUIRED_TOOLS=("list_incidents" "get_incident" "list_services" "list_oncalls" "list_teams" "list_users")
for tool in "${REQUIRED_TOOLS[@]}"; do
    if grep -q "pagerduty-mcp/$tool" ".github/agents/my-agent.md"; then
        echo "  ✓ Tool: pagerduty-mcp/$tool"
    else
        echo "  ✗ Tool NOT found: pagerduty-mcp/$tool"
        exit 1
    fi
done

# Check authentication configuration
echo "✓ Checking authentication configuration..."
if grep -q "auth:" ".github/agents/my-agent.md"; then
    echo "  ✓ Authentication configured"
else
    echo "  ✗ Authentication configuration NOT found"
    exit 1
fi

# Check demo service files
echo "✓ Checking demo service files..."
if [ -f "worker.c" ]; then
    echo "  ✓ worker.c found"
else
    echo "  ✗ worker.c NOT found"
    exit 1
fi

if [ -f "infra/kubernetes/deployment.yaml" ]; then
    echo "  ✓ Kubernetes deployment found"
else
    echo "  ✗ Kubernetes deployment NOT found"
    exit 1
fi

# Check for intentional memory leak (the bug that triggers incidents)
echo "✓ Checking for intentional memory leak in worker.c..."
if grep -q "malloc" "worker.c" && ! grep -q "free(buffer)" "worker.c"; then
    echo "  ✓ Memory leak present (as intended for testing)"
else
    echo "  ✗ Memory leak not found or already fixed"
    exit 1
fi

# Check documentation
echo "✓ Checking documentation..."
if [ -f "PAGERDUTY_MCP.md" ]; then
    echo "  ✓ PAGERDUTY_MCP.md found"
else
    echo "  ✗ PAGERDUTY_MCP.md NOT found"
    exit 1
fi

echo ""
echo "==================================="
echo "✓ All checks passed!"
echo "==================================="
echo ""
echo "PagerDuty MCP integration is properly configured."
echo "See PAGERDUTY_MCP.md for usage instructions."
echo ""
