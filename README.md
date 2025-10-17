# Demo Service to Test ADS (Automated Diagnostic System)

## Overview
This repository contains a demo worker service designed to test PagerDuty's Automated Diagnostic System (ADS) and Model Context Protocol (MCP) integration.

## Purpose
The service intentionally contains a memory leak to demonstrate:
- PagerDuty incident detection and response
- MCP-powered root cause analysis
- Automated remediation suggestions
- On-call team coordination

## Service Architecture
- **Language**: C
- **Deployment**: Kubernetes (minikube)
- **Container**: Alpine Linux with GCC
- **Resource Limits**: 64Mi memory, 250m CPU

## Known Issue
The `worker.c` service has an intentional memory leak:
```c
void controller() {
    while (1) {
        char *buffer = malloc(PAYLOAD_MB * 1024 * 1024 * sizeof(char));
        process_work(buffer);
        // BUG: Missing free(buffer) - causes OOMKilled incidents
    }
}
```

This causes the pod to be OOMKilled by Kubernetes, triggering a PagerDuty incident.

## Quick Start

### Prerequisites
- Docker
- minikube
- kubectl
- make

### Build and Deploy
```bash
# Build the Docker image and load into minikube
make build

# Deploy to Kubernetes
make deploy

# Monitor pod status (will see CrashLoopBackOff due to memory leak)
kubectl get pods -w -l app=worker-app

# View pod logs
kubectl logs -l app=worker-app

# Redeploy after changes
make redeploy

# Clean up
make delete
```

## PagerDuty MCP Integration

### What is MCP?
Model Context Protocol (MCP) enables PagerDuty to:
1. **Retrieve incident details** - Service, timeline, severity
2. **Identify on-call teams** - Who's responsible for the service
3. **Analyze code changes** - Recent commits, PRs, deployments
4. **Determine root cause** - Analyze code that likely caused the incident
5. **Suggest remediation** - Fix PRs or rollback recommendations

### MCP Analysis for This Service
When an OOMKilled incident occurs, MCP should:
1. Detect memory leak in `worker.c` line 26-27
2. Identify missing `free(buffer)` call
3. Correlate incident timing with pod restart events
4. Suggest adding memory deallocation
5. Tag on-call team members
6. Provide incident analysis with high confidence

### Documentation
- [PagerDuty MCP Integration Guide](PAGERDUTY_MCP.md)
- [Service Runbook](RUNBOOK.md)
- [Incident Analysis Template](incident-analysis-template.md)
- [PagerDuty Configuration](pagerduty-config.yaml)

## Testing the Integration
1. Deploy the service with `make deploy`
2. Service will start consuming memory
3. Pod will be OOMKilled within seconds
4. PagerDuty incident should be triggered
5. MCP analyzes the incident
6. Root cause identified: memory leak in controller()
7. Remediation suggested: Add `free(buffer)` call

## Expected MCP Output
```
Incident: #12345
Service: ads-demo-service
Severity: SEV-2
Root Cause: Memory leak in worker.c controller() function
File: worker.c
Line: 26-28
Confidence: High
Fix: Add free(buffer) after process_work(buffer)
On-Call: @team-member
```

## Files in This Repository
- `worker.c` - C worker program with memory leak
- `Dockerfile` - Container build configuration
- `Makefile` - Build and deployment commands
- `infra/kubernetes/deployment.yaml` - Kubernetes deployment config
- `PAGERDUTY_MCP.md` - PagerDuty MCP integration documentation
- `RUNBOOK.md` - Incident response runbook
- `incident-analysis-template.md` - Template for incident analysis
- `pagerduty-config.yaml` - PagerDuty integration configuration

## Contributing
This is a demo service. Contributions that enhance the PagerDuty integration testing capabilities are welcome.

## License
[License information]
