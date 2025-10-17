# PagerDuty MCP Integration

## Overview
This repository demonstrates PagerDuty's Model Context Protocol (MCP) integration for incident response and analysis.

## Service Description
- **Service Name**: ads-demo-service (Worker Service)
- **Purpose**: Demo service to test Automated Diagnostic System (ADS)
- **Known Issue**: Memory leak in worker.c causing OOMKilled incidents

## Incident Detection
The worker service is designed to trigger incidents due to:
1. **Memory Leak**: The `controller()` function allocates memory in an infinite loop without freeing it
2. **Resource Limits**: Kubernetes deployment limits memory to 64Mi
3. **Expected Behavior**: Pod will be OOMKilled and restarted repeatedly

## PagerDuty MCP Capabilities

### 1. Incident Retrieval
When an incident occurs, PagerDuty MCP can:
- Retrieve incident details including service, timeline, and description
- Identify affected service and severity level
- Track incident status and resolution timeline

### 2. On-Call Team Identification
- Identify on-call team responsible for the service
- Tag relevant team members for incident response
- Escalate based on severity and response time

### 3. Code Change Analysis
For this service, MCP should analyze:
- Recent commits to `worker.c`
- Kubernetes deployment changes
- Infrastructure modifications in `infra/kubernetes/`

### 4. Root Cause Analysis
**Known Issue in worker.c (Line 26):**
```c
char *buffer = malloc(PAYLOAD_MB * 1024 * 1024 * sizeof(char));
process_work(buffer);
// BUG: Memory is never freed! Should call: free(buffer);
```

### 5. Remediation Suggestions
MCP should suggest:
- **Fix**: Add `free(buffer)` after `process_work(buffer)` call
- **Rollback**: Revert to previous working version if available
- **Mitigation**: Increase memory limits temporarily (not recommended long-term)

## Testing PagerDuty MCP

### Expected Workflow
1. Deploy service with `make deploy`
2. Service will consume memory and trigger OOMKilled
3. Kubernetes events trigger PagerDuty incident
4. MCP analyzes incident and code
5. MCP identifies memory leak in worker.c
6. MCP suggests remediation PR with fix

### Incident Response Flow
```
Incident Triggered → MCP Activated → Code Analysis → Root Cause Identified → Fix Suggested
```

## Verification Checklist
- [ ] PagerDuty service integration configured
- [ ] Kubernetes monitoring enabled
- [ ] Alert rules configured for OOMKilled events
- [ ] MCP can access repository for code analysis
- [ ] On-call schedule configured
- [ ] Incident escalation policies defined

## Expected MCP Analysis Output
When analyzing an incident for this service, MCP should identify:
- **File**: `worker.c`
- **Function**: `controller()`
- **Line**: 26-27
- **Issue**: Memory allocation without corresponding free
- **Impact**: Continuous memory growth until OOMKilled
- **Confidence**: High (clear memory leak pattern)

## Remediation PR Format
```
Title: [Incident #ID] Fix memory leak in worker service
Description:
- Incident: [PagerDuty URL]
- Severity: [SEV level]
- Root Cause: Memory leak in controller() function
- Fix: Added free(buffer) to prevent memory leak
- Affected Service: ads-demo-service
- On-Call: @[team-member]
```

## Additional Resources
- PagerDuty Incident Documentation
- MCP Integration Guide
- Service Runbook
