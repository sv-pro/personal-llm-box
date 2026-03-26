---
title: "API Documentation"
tags: ["documentation", "api"]
created_at: 2026-02-01T10:00:00+00:00
---

# API Documentation

## Authentication Endpoints

### POST /auth/login
Authenticate user and receive JWT token.

**Request:**
```json
{
  "username": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "expires_in": 3600
}
```

### POST /auth/renew
Renew an existing JWT token.

**Request:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "expires_in": 3600
}
```

## Data Processing Endpoints

### POST /process/upload
Upload and process a file.

**Supported formats:** CSV, JSON, XML
**Max file size:** 100MB
**Timeout:** 300 seconds

**Request:**
Multipart form data with file field.

**Response:**
```json
{
  "status": "processed",
  "output_format": "json",
  "file_url": "/downloads/processed_file.json"
}
```

## Rate Limiting
All endpoints are rate-limited to 100 requests per minute per IP address. This is enforced by the API Gateway.

## Error Codes
- 401: Authentication failed
- 413: File too large
- 429: Rate limit exceeded
- 504: Processing timeout
