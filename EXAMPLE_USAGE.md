# Example Usage of Incident Lookup Tools

This document shows example outputs and usage patterns for the incident lookup tools.

## Prerequisites

Before using these tools, set your PagerDuty API token:

```bash
export PAGERDUTY_API_TOKEN="your-api-token-here"
```

## Example 1: Looking Up All Active Incidents

```bash
./incident-lookup.sh --service ads-demo-service
```

**Example Output:**

```
Looking up incidents for service: ads-demo-service
Status filter: triggered,acknowledged

Found service ID: P9ABCDEF
Found 2 incident(s):

================================================================================
Incident #42 - P1XYZABC
Title: ads-demo-service - OOMKilled - worker pod restarting
Status: triggered
Urgency: high
Service: ads-demo-service
Created: 2025-10-16T10:30:15Z
Last Updated: 2025-10-16T10:30:15Z
URL: https://your-domain.pagerduty.com/incidents/P1XYZABC
Description: Container worker-container in pod worker-deployment-abc123 was OOMKilled
Assignments:
  - Jane Doe (user)
================================================================================

================================================================================
Incident #43 - P1XYZDEF
Title: ads-demo-service - High CPU usage detected
Status: acknowledged
Urgency: low
Service: ads-demo-service
Created: 2025-10-16T12:15:30Z
Last Updated: 2025-10-16T12:20:45Z
URL: https://your-domain.pagerduty.com/incidents/P1XYZDEF
Description: CPU usage above 80% for 5 minutes
Assignments:
  - John Smith (user)
================================================================================

=== Incident Analysis ===
Total incidents: 2

By Status:
  triggered: 1
  acknowledged: 1

By Urgency:
  high: 1
  low: 1

=== Recommended Actions ===
1. Review incident timelines to identify patterns
2. Check recent deployments and correlate with incident creation times
3. Analyze common error patterns in incident descriptions
4. Review on-call assignments and ensure proper escalation

To analyze a specific incident in detail:
  ./incident-lookup.sh --incident-id <INCIDENT_ID>
```

## Example 2: Analyzing a Specific Incident with Git Correlation

```bash
python3 incident-analyzer.py --incident-id P1XYZABC
```

**Example Output:**

```
Analyzing incident: P1XYZABC
================================================================================

Incident #42 - P1XYZABC
Title: ads-demo-service - OOMKilled - worker pod restarting
Status: triggered
Urgency: high
Service: ads-demo-service
Created: 2025-10-16T10:30:15Z
Last Updated: 2025-10-16T10:30:15Z
URL: https://your-domain.pagerduty.com/incidents/P1XYZABC
Description: Container worker-container in pod worker-deployment-abc123 was OOMKilled

Assignments:
  - Jane Doe (user)

================================================================================
Analyzing commits from 2025-10-15 10:30:15 to 2025-10-16 10:30:15
================================================================================

Found 2 commit(s) in the 24 hours before the incident:

  SHA: a1b2c3d4
  Author: Developer Name <dev@example.com>
  Date: 2025-10-16 08:15:20 +0000
  Message: Increase payload size for testing

  SHA: e5f6g7h8
  Author: Developer Name <dev@example.com>
  Date: 2025-10-15 18:45:10 +0000
  Message: Update deployment configuration

================================================================================
Most Recent Commit Details:
================================================================================
commit a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
Author: Developer Name <dev@example.com>
Date:   Wed Oct 16 08:15:20 2025 +0000

    Increase payload size for testing

 worker.c | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)

diff --git a/worker.c b/worker.c
index 1234567..abcdefg 100644
--- a/worker.c
+++ b/worker.c
@@ -4,7 +4,7 @@
 #include <string.h>
 #include <unistd.h>
 
-#define PAYLOAD_MB 10
+#define PAYLOAD_MB 20
 
 void process_work(char *payload) {

================================================================================
Recommendations:
================================================================================

⚠️  Memory-related incident detected!
   Potential causes:
   - Memory leak in application
   - Insufficient memory limits in Kubernetes deployment
   - Check worker.c for malloc calls without corresponding free()

   Suggested actions:
   1. Review memory allocation patterns in worker.c
   2. Check Kubernetes memory limits in infra/kubernetes/deployment.yaml
   3. Run memory profiler (valgrind) to identify leaks
   4. Consider increasing memory limits or fixing the leak

📝 2 commit(s) found in 24h window before incident
   Suggested actions:
   1. Review the commits for potentially problematic changes
   2. Consider rolling back the most recent commit if correlation is strong
   3. Run tests on the commit before the changes

📊 Next Steps:
   1. Acknowledge the incident in PagerDuty if not already done
   2. Correlate incident time with deployment times
   3. Check application logs for error patterns
   4. Create a fix PR with title: [Incident #42] Fix for ads-demo-service - OOMKilled - worker pod restarting
   5. Tag on-call team members for review
```

## Example 3: Analyzing All Incidents for a Service

```bash
python3 incident-analyzer.py --service ads-demo-service --days 7
```

**Example Output:**

```
Analyzing incidents for service: ads-demo-service
Looking back 7 days from 2025-10-09T14:45:14.000000
================================================================================

Found 5 incident(s):

  #42 - triggered - high
    ads-demo-service - OOMKilled - worker pod restarting
    Created: 2025-10-16T10:30:15Z
    URL: https://your-domain.pagerduty.com/incidents/P1XYZABC

  #41 - resolved - high
    ads-demo-service - OOMKilled - worker pod restarting
    Created: 2025-10-15T08:20:10Z
    URL: https://your-domain.pagerduty.com/incidents/P1XYZAB0

  #40 - resolved - low
    ads-demo-service - High CPU usage detected
    Created: 2025-10-14T15:10:05Z
    URL: https://your-domain.pagerduty.com/incidents/P1XYZAB1

  #39 - resolved - high
    ads-demo-service - OOMKilled - worker pod restarting
    Created: 2025-10-13T11:05:30Z
    URL: https://your-domain.pagerduty.com/incidents/P1XYZAB2

  #38 - resolved - high
    ads-demo-service - OOMKilled - worker pod restarting
    Created: 2025-10-12T09:45:20Z
    URL: https://your-domain.pagerduty.com/incidents/P1XYZAB3

================================================================================
Incident Patterns:
================================================================================

By Status:
  triggered: 1
  resolved: 4

By Urgency:
  high: 4
  low: 1
```

## Example 4: Looking Up Incidents in a Date Range

```bash
./incident-lookup.sh --service ads-demo-service \
  --since 2025-10-10T00:00:00Z \
  --until 2025-10-15T23:59:59Z \
  --status triggered,acknowledged,resolved
```

This will show all incidents (including resolved ones) in the specified date range.

## Example 5: Responding to an OOM Incident

Complete workflow for responding to a memory-related incident:

```bash
# Step 1: Get incident details
python3 incident-analyzer.py --incident-id P1XYZABC

# Step 2: Check current code for memory leaks
grep -A 5 "malloc" worker.c

# Step 3: Verify the fix is applied
grep "free(buffer)" worker.c

# Step 4: If fix is present, rebuild and deploy
make build
make redeploy

# Step 5: Monitor the deployment
kubectl get pods -w
kubectl logs -f -l app=worker-app

# Step 6: Check memory usage
kubectl top pod -l app=worker-app

# Step 7: Once verified, update PagerDuty incident
# (Manual step: Go to PagerDuty UI and resolve incident with notes)
```

## Interpreting Results

### Memory Leak Indicators

If you see:
- Multiple OOMKilled incidents
- Increasing memory usage over time
- Incidents recurring after pod restarts

**Action**: Check for missing `free()` calls in C code or unbounded caches in application.

### Deployment Correlation

If incidents occur shortly after deployments:
- Check commits in the 24-hour window before incident
- Review recent code changes
- Consider rolling back to previous stable version

### Pattern Analysis

Use the incident analysis summary to identify:
- Frequency of incidents (daily, hourly)
- Common times (during high traffic, after deployments)
- Affected services or pods
- Correlation with external events

## Tips for Effective Incident Response

1. **Always correlate with deployments**: Use the git commit analysis to identify changes
2. **Check multiple incidents**: Look for patterns across similar incidents
3. **Monitor after fixes**: Ensure the issue doesn't recur
4. **Document in runbooks**: Add common patterns to INCIDENT_RESPONSE.md
5. **Update alerts**: Adjust thresholds based on incident patterns

## Troubleshooting

### "PAGERDUTY_API_TOKEN not set"

Set your token:
```bash
export PAGERDUTY_API_TOKEN="your-token-here"
```

### "Service not found"

Verify the service name in PagerDuty matches exactly (case-sensitive).

### "curl: command not found" or "jq: command not found"

Install required tools:
```bash
# On Ubuntu/Debian
apt-get install curl jq

# On macOS
brew install curl jq

# On Alpine
apk add curl jq
```

### Python script errors

Ensure Python 3.6+ is installed:
```bash
python3 --version
```

## Next Steps

After using these tools:
1. Review [INCIDENT_RESPONSE.md](INCIDENT_RESPONSE.md) for complete response workflows
2. Set up regular incident reviews (weekly/monthly)
3. Create runbooks for common incident types
4. Configure alerting thresholds based on incident patterns
5. Train team members on incident response procedures
