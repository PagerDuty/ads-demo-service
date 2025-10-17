# Demo service to test ADS

Testing

## Incident Response

### [Incident #Q0LB963CY3TJG2] Memory Leak Fix

**Issue**: The worker service was experiencing OOMKilled pod restarts due to a critical memory leak in the controller loop.

**Root Cause**: 
- Memory allocated via `malloc()` in the controller loop was never freed, causing memory to accumulate with each iteration (10MB per iteration)
- With a 64Mi memory limit in Kubernetes, the pod would crash after ~6 iterations
- Function signature mismatch between `process_work_item` declaration and usage

**Fix Applied**:
1. Added `free(buffer)` after `process_work(buffer)` to properly release allocated memory
2. Added NULL check for malloc failure to prevent crashes
3. Fixed `process_work_item` signature to match actual usage (char instead of char*)

**Confidence**: High - The memory leak is clearly identifiable in the code and directly correlates with OOMKilled symptoms

**Affected Service**: worker-deployment
**Severity**: Critical
**Status**: Fixed
