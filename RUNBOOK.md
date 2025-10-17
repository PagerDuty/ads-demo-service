# Worker Service Runbook

## Service Overview
- **Name**: ads-demo-service
- **Type**: C-based worker service
- **Purpose**: Demonstrates automated diagnostic capabilities with PagerDuty
- **Deployment**: Kubernetes via minikube

## Common Incidents

### Memory Leak / OOMKilled

#### Symptoms
- Pod restarts frequently
- Kubernetes events show OOMKilled
- Memory usage increases linearly over time
- Pod fails to stay running for more than a few seconds

#### Root Cause
The worker service has a memory leak in the `controller()` function at line 26-27 of `worker.c`:
```c
char *buffer = malloc(PAYLOAD_MB * 1024 * 1024 * sizeof(char));
process_work(buffer);
// Missing: free(buffer);
```

#### Resolution
1. **Immediate Fix**: Apply patch to add `free(buffer)` after line 27
2. **Deploy**: Rebuild and redeploy with `make build && make redeploy`
3. **Verify**: Monitor pod status with `kubectl get pods -w`

#### Prevention
- Code review should catch missing free() calls
- Add static analysis (valgrind, AddressSanitizer) in CI/CD
- Implement memory monitoring and alerting

### Build Failures

#### Symptoms
- Docker build fails
- Compilation errors in worker.c

#### Resolution
1. Check GCC version compatibility
2. Verify Alpine base image version
3. Review recent changes to worker.c
4. Test locally: `gcc -o worker worker.c`

### Deployment Failures

#### Symptoms
- kubectl apply fails
- Pods in CrashLoopBackOff
- ImagePullBackOff errors

#### Resolution
1. Verify image exists: `minikube image ls | grep worker`
2. Rebuild if needed: `make build`
3. Check deployment yaml syntax
4. Review pod logs: `kubectl logs -l app=worker-app`

## Monitoring & Alerts

### Key Metrics
- Memory usage (should stay under 64Mi limit)
- Pod restart count
- CPU usage
- Deployment status

### PagerDuty Integration
- Incidents auto-created for OOMKilled events
- Severity based on restart frequency
- On-call team notified automatically

## Quick Commands

### Build & Deploy
```bash
make build    # Build and load Docker image to minikube
make deploy   # Deploy to Kubernetes
make redeploy # Delete and redeploy
make delete   # Remove deployment
```

### Debugging
```bash
# Check pod status
kubectl get pods -l app=worker-app

# View pod logs
kubectl logs -l app=worker-app --tail=50

# Describe pod (see events)
kubectl describe pod -l app=worker-app

# Check resource usage
kubectl top pod -l app=worker-app
```

### Access minikube
```bash
minikube start
minikube dashboard
minikube image ls
```

## Escalation
- **L1**: Check pod status and logs
- **L2**: Review recent deployments and code changes
- **L3**: Deep dive into application code and memory profiling

## Related Documentation
- [PagerDuty MCP Integration](PAGERDUTY_MCP.md)
- [README](README.md)
