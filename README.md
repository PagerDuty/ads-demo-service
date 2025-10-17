# Demo service to test ADS

This is a demo service for testing the PagerDuty incident response workflow via GitHub Copilot agents with Model Context Protocol (MCP) integration.

## Overview

The service contains:
- A C-based worker with an intentional memory leak
- Kubernetes deployment configuration
- GitHub Copilot agent integrated with PagerDuty MCP

## Quick Start

```bash
# Build and load Docker image into minikube
make build

# Deploy to Kubernetes
make deploy

# Redeploy (delete and recreate)
make redeploy

# Delete deployment
make delete
```

## PagerDuty MCP Integration

This repository includes a GitHub Copilot agent that automatically responds to PagerDuty incidents by:
- Analyzing incident context
- Identifying recent code changes
- Suggesting fixes via GitHub PRs

See [PAGERDUTY_MCP.md](PAGERDUTY_MCP.md) for detailed documentation on the integration.

## Testing

The worker service is designed to trigger incidents for testing the PagerDuty incident response workflow.
