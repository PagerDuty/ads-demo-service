# PagerDuty MCP Verification Guide

## Purpose
This document provides a comprehensive verification checklist for PagerDuty's Model Context Protocol (MCP) integration with the ads-demo-service.

## MCP Integration Status

### ✅ Repository Setup
- [x] Service code exists (worker.c)
- [x] Known issue present (memory leak)
- [x] Kubernetes deployment configuration
- [x] Documentation created
- [x] PagerDuty configuration documented

### 📋 MCP Capabilities Verification

#### 1. Incident Retrieval
**Expected Behavior**: MCP should retrieve and display incident details

Test Query: "Show me details for incident #[ID]"

**Expected Response**:
```
Incident ID: [ID]
Service: ads-demo-service
Status: Triggered/Acknowledged/Resolved
Severity: SEV-2
Triggered: [timestamp]
Description: Worker pod OOMKilled - CrashLoopBackOff
```

**Verification**: ✅ Pass / ❌ Fail

---

#### 2. On-Call Team Identification
**Expected Behavior**: MCP should identify responsible team and members

Test Query: "Who is on-call for ads-demo-service?"

**Expected Response**:
```
Service: ads-demo-service
On-Call Team: [Team Name]
Primary: @[username]
Secondary: @[username]
Escalation Policy: [policy]
```

**Verification**: ✅ Pass / ❌ Fail

---

#### 3. Code Change Analysis
**Expected Behavior**: MCP should analyze recent commits and PRs

Test Query: "Show recent code changes to ads-demo-service in the last 24 hours"

**Expected Response**:
```
Recent Changes (24h lookback):
- Commit [SHA]: [message]
  Author: @[username]
  Files: worker.c, deployment.yaml
  Deployed: [Yes/No]
  
- PR #[num]: [title]
  Merged: [timestamp]
  Deployed: [timestamp]
```

**Verification**: ✅ Pass / ❌ Fail

---

#### 4. Root Cause Analysis
**Expected Behavior**: MCP should identify the memory leak

Test Query: "Analyze the root cause of incident #[ID] for ads-demo-service"

**Expected Response**:
```
Root Cause Analysis:
File: worker.c
Function: controller()
Lines: 26-28
Issue: Memory leak - malloc without free
Evidence: OOMKilled events, linear memory growth
Confidence: High

Code snippet:
void controller() {
    while (1) {
        char *buffer = malloc(PAYLOAD_MB * 1024 * 1024 * sizeof(char));
        process_work(buffer);
        // MISSING: free(buffer);
    }
}
```

**Verification**: ✅ Pass / ❌ Fail

---

#### 5. Remediation Suggestions
**Expected Behavior**: MCP should suggest a fix

Test Query: "Suggest remediation for incident #[ID]"

**Expected Response**:
```
Remediation Options:

1. Fix (Recommended):
   - Add free(buffer) after process_work(buffer)
   - File: worker.c, Line: 28
   - Impact: Prevents memory leak
   - Risk: Low
   
2. Rollback:
   - Revert to commit: [SHA]
   - Risk: Medium (if no previous stable version)
   
3. Mitigation:
   - Increase memory limit to 128Mi
   - Risk: High (masks underlying issue)

Recommended Action: Apply Fix #1
```

**Verification**: ✅ Pass / ❌ Fail

---

## Integration Test Scenarios

### Scenario 1: Fresh Incident
**Steps**:
1. Deploy service: `make deploy`
2. Wait for OOMKilled event (~30 seconds)
3. PagerDuty incident triggered
4. Query MCP: "Analyze incident #[ID]"
5. Verify MCP identifies memory leak

**Expected Outcome**: MCP correctly identifies root cause with high confidence

---

### Scenario 2: Recent Deployment Correlation
**Steps**:
1. Make a code change
2. Deploy with `make redeploy`
3. Incident occurs
4. Query MCP: "What changed before incident #[ID]?"
5. Verify MCP correlates deployment with incident

**Expected Outcome**: MCP shows recent commits and deployment timing

---

### Scenario 3: Fix Validation
**Steps**:
1. Apply fix (add `free(buffer)`)
2. Deploy fixed version
3. Monitor for 10 minutes
4. Query MCP: "Is incident #[ID] resolved?"
5. Verify MCP confirms no new OOMKilled events

**Expected Outcome**: MCP confirms service stability

---

## MCP Query Examples

### Basic Queries
```
"Show me active incidents for ads-demo-service"
"What's the status of incident #12345?"
"Who's on-call for ads-demo-service?"
"Show me the service health dashboard"
```

### Analysis Queries
```
"Analyze incident #12345 for ads-demo-service"
"What code changes happened before incident #12345?"
"Show me the root cause of the OOMKilled errors"
"What's causing the CrashLoopBackOff?"
```

### Remediation Queries
```
"Suggest a fix for incident #12345"
"Should I rollback or fix forward?"
"Create a PR to fix the memory leak"
"What's the recommended remediation?"
```

### Team Coordination Queries
```
"Notify on-call team about incident #12345"
"Who should review the fix PR?"
"Escalate incident #12345"
"Tag relevant team members"
```

---

## Success Criteria

### ✅ MCP Integration Complete When:
- [ ] MCP can retrieve incident details
- [ ] MCP identifies on-call team correctly
- [ ] MCP analyzes code changes within timeframe
- [ ] MCP detects memory leak in worker.c
- [ ] MCP suggests appropriate remediation
- [ ] MCP can correlate deployments with incidents
- [ ] MCP provides high-confidence root cause
- [ ] MCP generates incident analysis report
- [ ] MCP can tag team members in responses
- [ ] MCP integrates with GitHub for PR creation

---

## Troubleshooting

### Issue: MCP doesn't detect incident
**Check**:
- PagerDuty service integration configured
- Kubernetes monitoring enabled
- Webhook configured correctly
- Alert rules active

### Issue: MCP can't analyze code
**Check**:
- GitHub integration configured
- Repository access permissions
- MCP has read access to commits and PRs

### Issue: Root cause detection fails
**Check**:
- Service configuration in pagerduty-config.yaml
- File paths in analysis scope
- Sufficient context in incident description

---

## Performance Benchmarks

### Expected Response Times
- Incident retrieval: < 2 seconds
- On-call lookup: < 1 second
- Code analysis: < 5 seconds
- Root cause analysis: < 10 seconds
- Remediation suggestions: < 5 seconds

### Accuracy Targets
- Root cause detection: > 90% accuracy
- False positives: < 10%
- Confidence scoring: Calibrated correctly

---

## Next Steps

1. **Deploy Service**: Use `make deploy` to trigger incidents
2. **Monitor Events**: Watch for OOMKilled events
3. **Test MCP Queries**: Use query examples above
4. **Validate Responses**: Check against expected outputs
5. **Document Results**: Update verification status
6. **Iterate**: Refine configuration based on results

---

## Additional Resources

- [PagerDuty MCP Integration](PAGERDUTY_MCP.md)
- [Service Runbook](RUNBOOK.md)
- [Incident Analysis Template](incident-analysis-template.md)
- [PagerDuty Configuration](pagerduty-config.yaml)
- [PagerDuty Documentation](https://developer.pagerduty.com/)

---

**Document Version**: 1.0
**Last Updated**: 2025-10-17
**Status**: Ready for Testing
