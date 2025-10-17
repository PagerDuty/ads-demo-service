# PagerDuty MCP Integration - Documentation Index

This repository demonstrates a complete PagerDuty incident response system using GitHub Copilot agents with Model Context Protocol (MCP) integration.

## 📚 Documentation

### Quick Start
- **[README.md](README.md)** - Project overview and quick start guide
- **[CHECK_SUMMARY.md](CHECK_SUMMARY.md)** - Quick summary of PagerDuty MCP verification

### Detailed Documentation
- **[PAGERDUTY_MCP.md](PAGERDUTY_MCP.md)** - Complete integration guide
  - Overview and capabilities
  - How the integration works
  - Testing instructions
  - Example usage patterns
  - Verification checklist

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture
  - Component diagrams
  - Data flow diagrams
  - Request/response examples
  - Security and authentication
  - Testing procedures

- **[VERIFICATION_RESULTS.md](VERIFICATION_RESULTS.md)** - Verification report
  - Detailed checklist of all components
  - Status of each configuration element
  - Agent capabilities
  - Testing workflow

## 🔧 Tools & Scripts

- **[verify-pagerduty-mcp.sh](verify-pagerduty-mcp.sh)** - Automated verification script
  ```bash
  chmod +x verify-pagerduty-mcp.sh
  ./verify-pagerduty-mcp.sh
  ```

- **[Makefile](Makefile)** - Build and deployment commands
  ```bash
  make build      # Build and load Docker image
  make deploy     # Deploy to Kubernetes
  make redeploy   # Delete and redeploy
  make delete     # Remove deployment
  ```

## 📁 Source Files

### Application Code
- **[worker.c](worker.c)** - Demo worker with intentional memory leak
  - Allocates 10MB in loop without free()
  - Triggers OOM for incident testing

### Infrastructure
- **[Dockerfile](Dockerfile)** - Container build configuration
- **[infra/kubernetes/deployment.yaml](infra/kubernetes/deployment.yaml)** - Kubernetes deployment with 64Mi memory limit

### Configuration
- **[.github/agents/my-agent.md](.github/agents/my-agent.md)** - Agent configuration (private)
  - Agent name: `pagerduty-incident-responder`
  - MCP server URL and authentication
  - Available tools and capabilities

## 🎯 What Was Checked

The issue "check pagerduty mcp" requested verification of the PagerDuty Model Context Protocol integration. This PR confirms:

✅ Agent is properly configured  
✅ MCP server connection is set up  
✅ All required MCP tools are available  
✅ Authentication is configured  
✅ Demo service is ready for testing  
✅ Documentation is comprehensive  

## 🚀 Quick Reference

### Deploy and Test
```bash
# Build Docker image
make build

# Deploy to Kubernetes
make deploy

# Monitor for crashes (will happen after ~6-7 iterations)
kubectl get pods -w
kubectl logs -f deployment/worker-deployment

# After incident is created in PagerDuty
# Use the agent to analyze it
@pagerduty-incident-responder analyze incident #12345
```

### Agent Invocation
```
# Analyze specific incident
@pagerduty-incident-responder analyze incident #12345

# Check service status
@pagerduty-incident-responder check worker-deployment service

# List recent incidents
@pagerduty-incident-responder list recent incidents
```

### Expected Agent Behavior
1. Retrieves incident from PagerDuty via MCP
2. Identifies affected service and on-call engineer
3. Searches GitHub commits from last 24 hours
4. Analyzes code to find root cause (memory leak in worker.c)
5. Creates PR with fix: `[Incident #12345] Fix memory leak in worker controller`
6. Tags on-call engineer for review

## 📊 Integration Status

| Component | Status | Details |
|-----------|--------|---------|
| Agent Configuration | ✅ | `.github/agents/my-agent.md` |
| MCP Server | ✅ | `https://mcp.pagerduty.com/mcp` |
| PagerDuty Tools | ✅ | 6 tools configured |
| GitHub Tools | ✅ | 14 tools configured |
| Demo Service | ✅ | `worker.c` with memory leak |
| Kubernetes | ✅ | Deployment with 64Mi limit |
| Documentation | ✅ | 4 docs + verification script |

## 🔍 Key Files to Review

1. **Start here**: [CHECK_SUMMARY.md](CHECK_SUMMARY.md) - Quick overview
2. **Learn more**: [PAGERDUTY_MCP.md](PAGERDUTY_MCP.md) - Full guide
3. **Understand architecture**: [ARCHITECTURE.md](ARCHITECTURE.md) - System design
4. **Verify setup**: [VERIFICATION_RESULTS.md](VERIFICATION_RESULTS.md) - Detailed checks
5. **Test it**: [verify-pagerduty-mcp.sh](verify-pagerduty-mcp.sh) - Automated verification

## 💡 Understanding the Demo

This repository is intentionally designed to fail:
- `worker.c` has a memory leak (doesn't call `free()`)
- Kubernetes limits memory to 64Mi
- After ~6-7 loop iterations, OOM killer terminates the pod
- PagerDuty receives alert and creates incident
- Agent analyzes incident and suggests fix

This demonstrates the complete incident response workflow:
```
Code Bug → Service Crash → PagerDuty Alert → Agent Analysis → Fix PR
```

## 🎓 Learning Resources

- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [GitHub Copilot Agents Documentation](https://docs.github.com/copilot)
- [PagerDuty API Documentation](https://developer.pagerduty.com/)

## ✅ Verification

To verify the integration is working:

1. Run automated checks:
   ```bash
   ./verify-pagerduty-mcp.sh
   ```

2. Review documentation:
   - Read [CHECK_SUMMARY.md](CHECK_SUMMARY.md)
   - Review [VERIFICATION_RESULTS.md](VERIFICATION_RESULTS.md)

3. Test end-to-end:
   - Deploy service: `make build && make deploy`
   - Wait for incident
   - Invoke agent
   - Verify PR creation

## 📝 Summary

**Issue**: "check pagerduty mcp"  
**Status**: ✅ COMPLETE  
**Result**: PagerDuty MCP integration is properly configured and documented

All components are in place for automated incident response:
- PagerDuty MCP connection configured
- Agent with incident analysis capabilities
- Demo service for testing
- Comprehensive documentation
- Verification tooling

The integration was already correctly set up - this PR adds documentation to make it explicit, verifiable, and maintainable.
