# Incident Response Guide for ads-demo-service

This document describes how to look up and respond to incidents for the ads-demo-service.

## Prerequisites

1. **PagerDuty API Token**: You need a PagerDuty API token with read access to incidents
   - Get your token from: https://your-domain.pagerduty.com/api_keys
   - Set it as an environment variable: `export PAGERDUTY_API_TOKEN="your-token-here"`

2. **Required Tools**:
   - `curl` and `jq` (for bash script)
   - Python 3.6+ (for Python analyzer)
   - `git` (for correlating with commits)

3. **Quick Test**: Run `./test-incident-tools.sh` to verify all tools are present and configured correctly

> 💡 **Tip**: See [EXAMPLE_USAGE.md](EXAMPLE_USAGE.md) for detailed examples with sample output

## Looking Up Incidents

### Method 1: Using the Bash Script

The `incident-lookup.sh` script provides a quick way to look up incidents:

```bash
# Make the script executable
chmod +x incident-lookup.sh

# Look up all active incidents for the service
./incident-lookup.sh

# Look up a specific incident by ID
./incident-lookup.sh --incident-id PXXXXXX

# Look up incidents with custom filters
./incident-lookup.sh --service ads-demo-service --status triggered,acknowledged

# Look up incidents in a date range
./incident-lookup.sh --since 2025-10-01T00:00:00Z --until 2025-10-16T00:00:00Z

# Show help
./incident-lookup.sh --help
```

### Method 2: Using the Python Analyzer

The `incident-analyzer.py` script provides deeper analysis with git commit correlation:

```bash
# Make the script executable
chmod +x incident-analyzer.py

# Analyze a specific incident (includes git commit correlation)
python3 incident-analyzer.py --incident-id PXXXXXX

# Analyze all incidents for the service in the last 7 days
python3 incident-analyzer.py --service ads-demo-service

# Analyze incidents for the last 30 days
python3 incident-analyzer.py --service ads-demo-service --days 30
```

The Python analyzer will:
- Retrieve incident details from PagerDuty
- Find git commits in the 24 hours before the incident
- Correlate code changes with incident timing
- Identify common incident patterns (OOM, crashes, etc.)
- Provide recommendations for remediation

## Common Incident Types for ads-demo-service

### Memory Leak / OOMKilled Incidents

**Symptoms**:
- Pod restarts frequently
- Kubernetes OOMKilled events
- Incident title contains "memory" or "OOM"

**Root Cause**:
The worker.c application has a memory leak in the `controller()` function where allocated buffers are not freed.

**Remediation**:
1. Identify the incident and correlate with recent deployments
2. Check the fix in the latest version of worker.c
3. If using an old version, apply the memory leak fix:

```c
void controller() {
    while (1) {
        char *buffer = malloc(PAYLOAD_MB * 1024 * 1024 * sizeof(char));
        process_work(buffer);
        free(buffer);  // FIX: Free the allocated buffer
    }
}
```

4. Rebuild and redeploy:
```bash
make build
make redeploy
```

## Incident Response Workflow

1. **Detect and Acknowledge**
   - Receive PagerDuty alert
   - Acknowledge the incident
   - Use incident-lookup.sh or incident-analyzer.py to get details

2. **Analyze**
   ```bash
   # Get incident details with git correlation
   python3 incident-analyzer.py --incident-id PXXXXXX
   ```
   
   - Review incident description and error messages
   - Check git commits in the 24-hour window before the incident
   - Correlate with deployment times
   - Check Kubernetes pod logs: `kubectl logs -l app=worker-app`

3. **Diagnose**
   - For memory issues: Check memory usage and limits
   - For crashes: Review application logs
   - For performance: Check CPU usage and processing times

4. **Remediate**
   - If caused by recent deployment: Consider rollback
   - If known bug: Apply fix and create PR
   - If configuration issue: Update Kubernetes manifests
   
   PR Title format: `[Incident #123] Fix for <incident description>`

5. **Verify and Resolve**
   - Deploy the fix
   - Monitor service health
   - Verify incident is resolved
   - Update PagerDuty incident status

6. **Post-Mortem**
   - Document root cause
   - Add to runbook
   - Create preventive measures
   - Update monitoring/alerts if needed

## Example: Responding to an OOM Incident

```bash
# 1. Look up the incident
python3 incident-analyzer.py --incident-id P123456

# Output shows:
# - Incident: OOMKilled - worker pod restarting
# - Recent commit: Updated worker.c 2 hours before incident
# - Recommendation: Check memory allocation

# 2. Check the current memory leak
grep -A 5 "controller()" worker.c
# Shows: buffer is malloc'd but never freed

# 3. Apply the fix (add free(buffer))
# Edit worker.c to add: free(buffer);

# 4. Build and deploy
make build
make redeploy

# 5. Monitor
kubectl get pods -w
kubectl logs -f -l app=worker-app

# 6. Update PagerDuty incident with resolution notes
```

## Configuration

### Environment Variables

- `PAGERDUTY_API_TOKEN`: Your PagerDuty API token (required)
- `PAGERDUTY_SERVICE_NAME`: Service name to filter by (default: ads-demo-service)

### Service Configuration

The service configuration in PagerDuty should include:
- Service name: `ads-demo-service`
- Integration type: Kubernetes monitoring
- Escalation policy with on-call schedule
- Alert grouping by incident type

## Monitoring and Alerts

Key metrics to monitor:
- Pod memory usage (set alert at 80% of limit)
- Pod restart count
- Container OOMKilled events
- Application error rate

Current limits (from infra/kubernetes/deployment.yaml):
- Memory limit: 64Mi
- CPU limit: 250m

## Known Issues

1. **Memory Leak in worker.c**
   - Status: Fixed in latest version
   - Impact: Causes OOMKilled after ~640 iterations
   - Fix: Added `free(buffer)` in controller loop

2. **Process Work Item Signature**
   - Status: Known issue
   - Impact: Incorrect parameter type (char * vs char)
   - Fix: Change parameter type or pass-by-value

## References

- PagerDuty API Documentation: https://developer.pagerduty.com/api-reference/
- Kubernetes Troubleshooting: https://kubernetes.io/docs/tasks/debug/
- Repository: https://github.com/PagerDuty/ads-demo-service
