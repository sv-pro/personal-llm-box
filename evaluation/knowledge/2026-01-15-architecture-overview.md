---
title: "System Architecture Overview"
tags: ["architecture", "design"]
created_at: 2026-01-15T10:00:00+00:00
---

# System Architecture Overview

Our application follows a microservices architecture with three main components:

## Authentication Service
- Handles user login and registration
- Uses JWT tokens for session management
- Database: PostgreSQL users table
- Port: 8001

## API Gateway
- Routes requests to appropriate services
- Implements rate limiting
- Port: 8000

## Data Processing Service
- Processes uploaded files
- Converts formats (CSV, JSON, XML)
- Port: 8002

## Technology Stack
- Python 3.11
- FastAPI framework
- Redis for caching
- PostgreSQL for persistence

## Known Limitations
The authentication service currently has a memory leak when processing large batches of token renewals. This was first reported in the January sprint planning.
