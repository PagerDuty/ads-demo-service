# PagerDuty MCP Integration

This repository includes a GitHub Copilot agent that integrates with PagerDuty via the Model Context Protocol (MCP).

## Overview

The `pagerduty-incident-responder` agent is configured to:
- Connect to PagerDuty's MCP server at `https://mcp.pagerduty.com/mcp`
- Retrieve incident information and on-call data
- Analyze code changes that may have caused incidents
- Suggest fixes and create remediation PRs

## Agent Configuration

The agent is configured in `.github/agents/my-agent.md` with the following capabilities:

### MCP Tools Available
- `pagerduty-mcp/list_incidents` - List active incidents
- `pagerduty-mcp/get_incident` - Get details for a specific incident
- `pagerduty-mcp/list_services` - List PagerDuty services
- `pagerduty-mcp/list_oncalls` - List on-call schedules
- `pagerduty-mcp/list_teams` - List teams
- `pagerduty-mcp/list_users` - List users

### Authentication
The MCP server uses SSE (Server-Sent Events) with header-based authentication.

## How It Works

1. **Incident Detection**: When an incident occurs in PagerDuty affecting this service
2. **Context Retrieval**: The agent retrieves incident details, affected service, and on-call information
3. **Code Analysis**: Searches GitHub for recent commits within 24 hours before incident
4. **Root Cause Analysis**: Identifies likely code changes that caused the issue
5. **Remediation**: Creates a PR with fix or rollback, titled `[Incident #ID] Fix for [description]`

## Demo Service

This repository contains a demo worker service (`worker.c`) that intentionally:
- Allocates 10MB of memory in a loop
- Never frees allocated memory (memory leak)
- Runs in Kubernetes with a 64Mi memory limit
- Designed to trigger OOM (Out of Memory) incidents

This allows testing the incident response workflow:
```
Memory leak → OOM Kill → PagerDuty Alert → Agent Analysis → Suggested Fix
```

## Testing the Integration

To test the PagerDuty MCP integration:

1. Deploy the service: `make build && make deploy`
2. Wait for memory leak to trigger OOM kill
3. Verify PagerDuty incident is created
4. Use the GitHub Copilot agent to analyze the incident
5. Agent should identify `worker.c` memory leak as root cause
6. Agent should suggest adding `free(buffer)` in the controller loop

## Example Usage

When an incident occurs, you can ask the agent:
```
@pagerduty-incident-responder analyze incident #12345
```

Or for a service:
```
@pagerduty-incident-responder check worker-deployment service
```

The agent will:
- Retrieve incident details from PagerDuty
- Identify the on-call engineer
- Search for recent commits to this repository
- Analyze the memory leak in `worker.c`
- Suggest a fix PR with proper memory management

## Known Issues

The current `worker.c` has an intentional memory leak at line 26-27:
```c
char *buffer = malloc(PAYLOAD_MB * 1024 * 1024 * sizeof(char));
process_work(buffer);
// Missing: free(buffer);
```

This is by design for testing incident response workflows.

## Verification Checklist

- [x] Agent configuration file exists at `.github/agents/my-agent.md`
- [x] MCP server URL configured: `https://mcp.pagerduty.com/mcp`
- [x] MCP tools properly defined in agent configuration
- [x] Authentication method specified (header-based SSE)
- [x] Demo service with intentional bug exists (`worker.c`)
- [x] Kubernetes deployment configured with memory limits
- [x] Documentation created for integration usage

## Architecture

```
┌─────────────────┐
│  GitHub Issues  │
│  / PR Comments  │
└────────┬────────┘
         │
         v
┌─────────────────────────┐
│  GitHub Copilot Agent   │
│  pagerduty-incident-    │
│  responder              │
└─────────┬───────────────┘
          │
          ├─────────────┬──────────────┐
          │             │              │
          v             v              v
┌──────────────┐ ┌──────────┐ ┌──────────────┐
│ PagerDuty    │ │ GitHub   │ │ Repository   │
│ MCP Server   │ │ API      │ │ Code Search  │
└──────────────┘ └──────────┘ └──────────────┘
```
