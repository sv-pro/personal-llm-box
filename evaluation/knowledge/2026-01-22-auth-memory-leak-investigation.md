---
title: "Auth Service Memory Leak Investigation"
tags: ["debugging", "authentication"]
created_at: 2026-01-22T09:15:00+00:00
---

# Memory Leak Investigation - Authentication Service

**Issue:** Memory consumption grows unbounded during token renewal operations
**Assigned to:** Alex
**Started:** 2026-01-22

## Reproduction Steps
1. Start auth service
2. Send 1000+ token renewal requests within 5 minutes
3. Monitor memory usage with `htop`
4. Observe memory growth from 200MB to 1.5GB+

## Findings

### Root Cause
The issue is in the `TokenCache` class. When tokens are renewed, old entries are not being garbage collected. The cache uses a dictionary that grows indefinitely.

### Code Location
File: `auth_service/token_manager.py`
Class: `TokenCache`
Method: `renew_token()`

The problematic pattern:
```python
self.token_cache[user_id] = new_token
# Missing: cleanup of expired tokens
```

### Solution
Implemented an LRU cache with max size of 10,000 entries. Also added a background task that runs every 5 minutes to remove expired tokens.

### Testing
Ran load test with 5000 token renewals. Memory usage remained stable at ~250MB.

## Status
**RESOLVED** - 2026-01-22 16:45

Fix deployed to staging. Awaiting production deployment approval from Taylor.
