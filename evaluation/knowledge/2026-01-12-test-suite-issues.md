---
title: "Test Suite Issues - January"
tags: ["testing", "quality"]
created_at: 2026-01-12T16:00:00+00:00
---

# Test Suite Issues

**Date:** 2026-01-12
**Reporter:** Jordan

## Memory Leak in Integration Tests

We've discovered a memory leak in our integration test suite. When running the full test suite, memory usage grows from 500MB to 2.5GB by the end of the run.

###Root Cause
The test fixtures are not being properly cleaned up after each test. Database connections remain open and cached data is not released.

### Impact
- Test suite takes 15 minutes to run (used to be 8 minutes)
- CI pipeline fails on small workers (2GB RAM limit)
- Developers avoid running full test suite locally

### Fix Applied
Added proper teardown methods to all test fixtures:

```python
def teardown():
    db.close_all_connections()
    cache.clear()
    logger.flush()
```

### Status
**RESOLVED** - 2026-01-12

Tests now run in 9 minutes with stable 600MB memory usage.

## Network Timeout in End-to-End Tests

E2E tests occasionally fail with network timeouts when testing external API integrations.

**Error:**
```
TimeoutError: Request to api.external-service.com timed out after 30 seconds
```

### Analysis
External service is occasionally slow (>30s response time). Our tests have a hardcoded 30-second timeout.

### Decision
Increased E2E test timeout to 60 seconds. Also added retry logic (3 attempts with exponential backoff).

### Status
**RESOLVED** - 2026-01-12

E2E test flakiness reduced from 15% to <2%.
