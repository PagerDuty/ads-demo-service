# PagerDuty MCP Integration Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Incident Response Workflow                    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────┐
│  Kubernetes     │
│  Cluster        │
│                 │
│  ┌───────────┐  │
│  │ worker    │  │
│  │ Pod       │  │
│  │ (64Mi)    │  │
│  └─────┬─────┘  │
│        │ OOM    │
│        │ Kill   │
└────────┼────────┘
         │
         v
┌─────────────────┐
│  Monitoring     │
│  & Alerting     │
│                 │
│  Detects OOM    │
└────────┬────────┘
         │
         │ Trigger Alert
         v
┌─────────────────────────────────────────────────────────────────┐
│                        PagerDuty                                 │
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│  │  Incident    │    │  On-Call     │    │   Teams      │     │
│  │   #12345     │    │  Schedule    │    │   & Users    │     │
│  └──────────────┘    └──────────────┘    └──────────────┘     │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │           PagerDuty MCP Server                         │    │
│  │        https://mcp.pagerduty.com/mcp                   │    │
│  │                                                         │    │
│  │  Exposes:                                               │    │
│  │  • list_incidents    • list_oncalls                    │    │
│  │  • get_incident      • list_teams                      │    │
│  │  • list_services     • list_users                      │    │
│  └────────────┬───────────────────────────────────────────┘    │
└───────────────┼──────────────────────────────────────────────┘
                │
                │ SSE Connection (Server-Sent Events)
                │ with Header Authentication
                v
┌─────────────────────────────────────────────────────────────────┐
│              GitHub Copilot Agent Framework                      │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Agent: pagerduty-incident-responder                   │    │
│  │  Config: .github/agents/my-agent.md                    │    │
│  │                                                         │    │
│  │  Capabilities:                                          │    │
│  │  • Query PagerDuty via MCP                             │    │
│  │  • Search GitHub commits/PRs                           │    │
│  │  • Analyze code changes                                │    │
│  │  • Create remediation PRs                              │    │
│  └────────────┬───────────────────────────────────────────┘    │
└───────────────┼──────────────────────────────────────────────┘
                │
                │ Invoked by user mention
                v
┌─────────────────────────────────────────────────────────────────┐
│                    GitHub Repository                             │
│                  PagerDuty/ads-demo-service                      │
│                                                                  │
│  User: @pagerduty-incident-responder analyze incident #12345    │
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│  │  worker.c    │    │  Recent      │    │  Deployment  │     │
│  │              │◄───┤  Commits     │    │  History     │     │
│  │ Memory Leak  │    │              │    │              │     │
│  └──────────────┘    └──────────────┘    └──────────────┘     │
│                                                                  │
│  Agent Actions:                                                  │
│  1. Get incident details from PagerDuty                         │
│  2. List commits in last 24 hours                               │
│  3. Identify memory leak in worker.c                            │
│  4. Create fix PR with free(buffer)                             │
│  5. Tag on-call engineer                                        │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Pull Request Created:                                 │    │
│  │  [Incident #12345] Fix memory leak in worker           │    │
│  │                                                         │    │
│  │  Changes:                                               │    │
│  │  + free(buffer);  // After process_work()             │    │
│  │                                                         │    │
│  │  @on-call-engineer for review                         │    │
│  └────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Demo Service (worker.c)
- **Purpose**: Simulate a faulty service
- **Behavior**: Allocates 10MB memory in infinite loop
- **Bug**: Never calls `free(buffer)` - intentional memory leak
- **Result**: Exceeds 64Mi Kubernetes limit → OOM kill

### 2. Kubernetes Deployment
- **Resource Limit**: 64Mi memory, 250m CPU
- **Restart Policy**: Always (restarts after crash)
- **Image Pull Policy**: IfNotPresent (uses local image)

### 3. PagerDuty
- **Incident Creation**: Triggered by monitoring/alerting system
- **MCP Server**: Provides API access via Model Context Protocol
- **Authentication**: Header-based (configured in agent)

### 4. GitHub Copilot Agent
- **Name**: pagerduty-incident-responder
- **Location**: `.github/agents/my-agent.md`
- **Tools**: 6 PagerDuty MCP tools + 14 GitHub tools
- **Trigger**: User mentions (e.g., `@pagerduty-incident-responder`)

### 5. Incident Response Flow
```
Crash → Alert → PagerDuty → User mentions Agent → Agent queries MCP
  ↓
Agent searches GitHub commits
  ↓
Agent identifies root cause
  ↓
Agent creates fix PR
  ↓
Agent tags on-call engineer
```

## Data Flow

### PagerDuty MCP Request
```
Agent → PagerDuty MCP Server
GET /mcp (via SSE)
Tool: pagerduty-mcp/get_incident
Params: { incident_id: "12345" }

Response:
{
  "id": "12345",
  "title": "worker-deployment OOM Killed",
  "status": "triggered",
  "urgency": "high",
  "service": { "name": "worker-deployment" },
  "created_at": "2025-10-17T14:30:00Z"
}
```

### GitHub Code Search
```
Agent → GitHub API
GET /repos/PagerDuty/ads-demo-service/commits
since: "2025-10-16T14:30:00Z" (24h before incident)

Response: List of recent commits
Agent analyzes: worker.c changes
```

### PR Creation
```
Agent → GitHub API
POST /repos/PagerDuty/ads-demo-service/pulls
{
  "title": "[Incident #12345] Fix memory leak in worker",
  "body": "Fixes memory leak causing OOM kills...",
  "head": "fix/incident-12345",
  "base": "main"
}
```

## Security

### Authentication
- **MCP Connection**: Header-based authentication (token not stored in repo)
- **GitHub Access**: Agent runs with GitHub App credentials
- **Secrets**: Managed by GitHub Copilot infrastructure

### Permissions
The agent requires:
- **PagerDuty**: Read access to incidents, services, on-call schedules
- **GitHub**: Read/write access to code, commits, PRs

## Testing the Integration

### Prerequisites
- Kubernetes cluster (minikube recommended)
- PagerDuty account with MCP enabled
- GitHub Copilot with agent access

### Test Steps
1. **Deploy Service**
   ```bash
   make build && make deploy
   ```

2. **Monitor for Crash**
   ```bash
   kubectl get pods -w
   kubectl logs -f worker-deployment-xxx
   ```

3. **Verify PagerDuty Incident**
   - Check PagerDuty dashboard
   - Note incident ID

4. **Invoke Agent**
   ```
   @pagerduty-incident-responder analyze incident #[ID]
   ```

5. **Verify Agent Response**
   - Agent retrieves incident from PagerDuty
   - Agent searches recent commits
   - Agent identifies worker.c:26-27 as root cause
   - Agent creates PR with fix
   - Agent tags on-call engineer

## Expected Results

### Agent Analysis Output
```
📊 Incident Analysis: #12345

🔴 Severity: HIGH
⏰ Started: 2025-10-17 14:30:00 UTC
🎯 Service: worker-deployment

🔍 Root Cause Analysis:
Memory leak in worker.c controller() function:
- Line 26: malloc(10MB) called in infinite loop
- Line 27: process_work() uses buffer
- Missing: free(buffer) after use

📝 Recent Changes:
No recent commits to worker.c - this is an existing bug

✅ Suggested Fix:
Add `free(buffer);` after line 27 in controller()

🔧 Creating PR: [Incident #12345] Fix memory leak in worker
👤 On-call: @engineer-username
```

### Generated PR
```markdown
# [Incident #12345] Fix memory leak in worker controller

## Context
PagerDuty Incident: https://[org].pagerduty.com/incidents/12345
Service: worker-deployment
Severity: HIGH

## Root Cause
Memory leak in `worker.c` line 26-27. The controller() function allocates
10MB buffers in an infinite loop but never frees them, causing OOM kills.

## Fix
Added `free(buffer);` after `process_work(buffer);` to properly release memory.

## Testing
- Deployed to staging
- Monitored memory usage - stable at ~10MB
- No OOM kills observed

@on-call-engineer please review

Fixes: #12345
```

## Monitoring & Alerts

After fixing, monitor for:
- Memory usage stable around 10MB
- No OOM kills in logs
- Incident marked as resolved in PagerDuty
- No new incidents for worker-deployment

## References

- [PAGERDUTY_MCP.md](PAGERDUTY_MCP.md) - Integration guide
- [CHECK_SUMMARY.md](CHECK_SUMMARY.md) - Verification summary
- [VERIFICATION_RESULTS.md](VERIFICATION_RESULTS.md) - Detailed checks
- [Model Context Protocol](https://modelcontextprotocol.io/) - MCP specification
