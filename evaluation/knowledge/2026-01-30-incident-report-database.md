---
title: "Incident Report: Database Connection Pool Exhaustion"
tags: ["incident", "database"]
created_at: 2026-01-30T22:00:00+00:00
---

# Incident Report: Database Connection Pool Exhaustion

**Incident ID:** INC-2026-001
**Date:** 2026-01-30
**Severity:** HIGH
**Duration:** 45 minutes (21:15 - 22:00)

## Summary

The API Gateway became unresponsive due to database connection pool exhaustion. All requests received 503 Service Unavailable errors.

## Timeline

**21:15** - AlertManager triggered: "API Gateway response time >500ms"
**21:18** - On-call engineer (Taylor) acknowledged alert
**21:22** - Identified root cause: Connection pool maxed out (100/100 connections)
**21:25** - Emergency fix: Increased pool size to 200
**21:30** - Service recovering, response times improving
**21:45** - All metrics back to normal
**22:00** - Incident closed

## Root Cause

The API Gateway connection pool was configured for 100 max connections. A sudden spike in traffic (3x normal load) from a promotional campaign caused all connections to be consumed.

**Contributing factors:**
- Connection timeout too high (60s, should be 30s)
- No connection pool monitoring/alerting
- Promotional campaign not communicated to engineering team

## Impact

- 45 minutes of service degradation
- ~2,700 failed requests (estimated)
- 3 customer complaints

## Resolution

**Immediate:**
- Increased connection pool to 200
- Reduced connection timeout to 30s

**Permanent:**
- Added connection pool metrics to monitoring dashboard
- Created alert: "Connection pool usage >80%"
- Documented capacity limits
- Added load testing for 5x traffic scenarios

## Action Items

1. **Load testing** - Simulate 10x traffic (Taylor, Due: 2026-02-07)
2. **Auto-scaling** - Implement dynamic connection pool sizing (Alex, Due: 2026-02-14)
3. **Communication** - Create marketing → engineering notification process (Sarah, Due: 2026-02-07)
4. **Documentation** - Update runbook with connection pool troubleshooting (Taylor, Due: 2026-02-03)

## Lessons Learned

**What went well:**
- Fast identification of root cause (<10 minutes)
- Emergency fix was effective
- Team communication was clear

**What could be improved:**
- Should have been monitoring connection pool usage
- Promotional campaign should have triggered capacity review
- Need automated scaling for sudden traffic spikes

## Preventive Measures

To prevent similar incidents:
- Monitor ALL connection pool metrics
- Review capacity before marketing campaigns
- Implement auto-scaling policies
- Regular load testing (monthly)
- Document capacity limits for all services
