# Verification Plan for personal-llm-box

**Date:** 2026-03-25
**Status:** Ready for execution
**Purpose:** Ensure all components work correctly before production use

---

## Executive Summary

The codebase is **100% complete** with all documented features implemented. This plan outlines systematic verification steps to confirm:
1. Docker services start correctly
2. The Ollama model is available
3. All API endpoints function as designed
4. Git-based storage works correctly
5. LLM integration produces valid responses

---

## Prerequisites Check

### System Requirements
- [ ] Docker Engine installed (version 20.10+)
- [ ] Docker Compose installed (version 2.0+)
- [ ] At least 8GB free disk space (for Ollama model)
- [ ] Ports 3000, 8000, 11434 available

### Verification Commands
```bash
docker --version
docker compose version
df -h .
netstat -tuln | grep -E ':(3000|8000|11434)'
```

---

## Phase 1: Service Startup (10-15 minutes)

### 1.1 Start All Services
```bash
cd /home/dev/code/sv-pro/personal-llm-box
docker compose up -d
```

**Expected Output:**
```
✔ Network personal-llm-box_default    Created
✔ Volume personal-llm-box_ollama_data Created
✔ Volume personal-llm-box_open_webui_data Created
✔ Container personal-llm-box-ollama-1  Started
✔ Container personal-llm-box-open-webui-1  Started
✔ Container personal-ai-box-backend  Started
```

**Verification:**
```bash
docker compose ps
```

All three services should show status "running" or "Up".

---

### 1.2 Download Ollama Model (First Run Only)
```bash
docker exec personal-llm-box-ollama-1 ollama pull qwen3:8b
```

**Expected:** Progress bars showing download, ~4.7GB model size
**Duration:** 5-10 minutes depending on network speed

**Verification:**
```bash
docker exec personal-llm-box-ollama-1 ollama list
```

Should show `qwen3:8b` in the list.

---

### 1.3 Check Service Logs
```bash
# Backend logs
docker compose logs backend

# Ollama logs
docker compose logs ollama

# Open WebUI logs
docker compose logs open-webui
```

**Look For:**
- Backend: `Uvicorn running on http://0.0.0.0:8000`
- Backend: No Python exceptions or import errors
- Ollama: `Listening on [::]:11434`
- Open WebUI: No fatal errors

---

## Phase 2: API Endpoint Testing

### 2.1 Health Check Endpoint
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{"status":"ok"}
```

**Status Code:** 200 OK

---

### 2.2 Save Artifact Endpoint
```bash
curl -X POST http://localhost:8000/artifact/save \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Verification Test",
    "content": "This is a test artifact created during verification.\n\nIt has multiple paragraphs.",
    "tags": ["test", "verification"]
  }'
```

**Expected Response:**
```json
{
  "status": "saved",
  "filename": "2026-03-25-verification-test.md"
}
```

**Verification:**
```bash
ls -la knowledge/
cat knowledge/2026-03-25-verification-test.md
```

**Expected File Content:**
```markdown
---
title: Verification Test
tags:
- test
- verification
created_at: '2026-03-25T...'
---

This is a test artifact created during verification.

It has multiple paragraphs.
```

**Git Check:**
```bash
cd knowledge
git log --oneline -1
git status
```

Should show a commit for the artifact and a clean working tree.

---

### 2.3 Ingest Endpoint
```bash
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Paragraph one with some content.\n\nParagraph two with more details.\n\nParagraph three to verify chunking."
  }'
```

**Expected Response:**
```json
{
  "status": "ingested",
  "filename": "ingested-20260325-HHMMSS.md",
  "chunks": 3
}
```

**Verification:**
```bash
ls -la knowledge/ingested-*.md
cat knowledge/ingested-*.md
```

File should contain three paragraphs with "ingested" tag.

---

### 2.4 Search Endpoint
```bash
# Search for content from previous tests
curl "http://localhost:8000/search?q=verification"
```

**Expected Response:**
```json
{
  "query": "verification",
  "results": [
    {
      "filename": "2026-03-25-verification-test.md",
      "snippet": "This is a test artifact created during verification.\nIt has multiple paragraphs."
    }
  ]
}
```

**Additional Tests:**
```bash
# Case-insensitive search
curl "http://localhost:8000/search?q=VERIFICATION"

# No results
curl "http://localhost:8000/search?q=nonexistent"

# Empty query (should fail validation)
curl "http://localhost:8000/search?q="
```

---

### 2.5 Digest Endpoint (LLM Integration)

**Note:** This is the most critical test as it verifies Ollama integration.

```bash
curl -X POST http://localhost:8000/digest \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I need to prepare for the upcoming product launch. The marketing team wants new landing page designs. The engineering team is blocked on API rate limits. Customer support reported 15 bug tickets this week."
  }'
```

**Expected Response Structure:**
```json
{
  "summary": "A 2-3 sentence summary...",
  "signals": [
    "Product launch is upcoming",
    "Marketing needs landing page designs",
    "Engineering blocked on API rate limits",
    "15 customer bug tickets reported"
  ],
  "actions": [
    "Coordinate with marketing on landing page timeline",
    "Investigate and resolve API rate limit issues",
    "Prioritize and triage the 15 bug tickets"
  ]
}
```

**Validation:**
- Response is valid JSON
- Contains `summary`, `signals`, `actions` keys
- `signals` is a non-empty array
- `actions` is a non-empty array
- Content is relevant to input text

**Error Scenario Test:**
```bash
# Empty text
curl -X POST http://localhost:8000/digest \
  -H "Content-Type: application/json" \
  -d '{"text": ""}'
```

Should return a digest (even for empty input, LLM should handle gracefully).

---

## Phase 3: Storage Verification

### 3.1 Git Repository Status
```bash
cd knowledge
git status
git log --oneline -5
```

**Expected:**
- Clean working tree
- At least 2 commits (artifact + ingest from tests)
- Commit messages should reference filenames

---

### 3.2 File Format Validation
```bash
cd knowledge
head -10 *.md
```

**Check:**
- All files start with `---` (YAML frontmatter)
- Frontmatter contains `title`, `tags`, `created_at`
- Frontmatter ends with `---`
- Content follows after blank line

---

### 3.3 Filename Convention Check
```bash
ls -1 knowledge/*.md
```

**Expected Patterns:**
- Artifacts: `YYYY-MM-DD-slug-here.md`
- Ingested: `ingested-YYYYMMDD-HHMMSS.md`

---

## Phase 4: Open WebUI Verification

### 4.1 Access Web Interface
```bash
# Open browser to:
http://localhost:3000
```

**Expected:**
- Login/signup page loads
- No connection errors
- Can create account

---

### 4.2 Chat Functionality
1. Create an account or sign in
2. Start a new chat
3. Verify model `qwen3:8b` is available
4. Send a test message: "Hello, can you introduce yourself?"

**Expected:**
- Model responds with generated text
- No connection errors to Ollama

---

## Phase 5: Error Handling Tests

### 5.1 Invalid JSON to Digest
```bash
curl -X POST http://localhost:8000/digest \
  -H "Content-Type: application/json" \
  -d 'not valid json'
```

**Expected:** 422 Unprocessable Entity (FastAPI validation error)

---

### 5.2 Missing Required Fields
```bash
curl -X POST http://localhost:8000/artifact/save \
  -H "Content-Type: application/json" \
  -d '{"title": "Only Title"}'
```

**Expected:** 422 Unprocessable Entity (missing `content`)

---

### 5.3 Service Resilience Test
```bash
# Stop Ollama temporarily
docker stop personal-llm-box-ollama-1

# Try digest endpoint
curl -X POST http://localhost:8000/digest \
  -H "Content-Type: application/json" \
  -d '{"text": "test"}'

# Restart Ollama
docker start personal-llm-box-ollama-1
```

**Expected:** 502 Bad Gateway error when Ollama is down, success after restart.

---

## Phase 6: Performance & Resource Check

### 6.1 Container Resource Usage
```bash
docker stats --no-stream
```

**Look For:**
- Ollama: High memory usage (4-8GB normal for LLM)
- Backend: Low memory (<200MB)
- Open WebUI: Moderate memory (~500MB)

---

### 6.2 Disk Space Check
```bash
du -sh knowledge/
docker system df -v | grep personal-llm-box
```

**Expected:**
- Knowledge directory starts small, grows with content
- Ollama volume ~5GB (model storage)

---

## Phase 7: Cleanup & Restart Test

### 7.1 Stop Services
```bash
docker compose down
```

**Expected:** All containers stop gracefully.

---

### 7.2 Restart Verification
```bash
docker compose up -d
sleep 10  # Wait for startup
curl http://localhost:8000/health
```

**Expected:**
- Services start successfully
- Health check passes immediately
- Knowledge directory persists with previous data
- No model re-download required

---

### 7.3 Data Persistence Check
```bash
curl "http://localhost:8000/search?q=verification"
```

**Expected:** Previously saved artifacts are still searchable.

---

## Success Criteria

The system is verified as working if:

- ✅ All three Docker services start without errors
- ✅ Health endpoint returns 200 OK
- ✅ Artifact save creates markdown files with correct format
- ✅ Ingested text is chunked and saved properly
- ✅ Search returns relevant results from knowledge base
- ✅ Digest endpoint produces valid JSON with summary/signals/actions
- ✅ Git commits are created for each save
- ✅ YAML frontmatter is properly formatted in all files
- ✅ Filename conventions are followed
- ✅ Open WebUI can communicate with Ollama
- ✅ Services survive restart with data intact
- ✅ Error handling works for invalid inputs

---

## Common Issues & Troubleshooting

### Issue: "Connection refused" on Ollama
**Solution:** Wait 30 seconds after `docker compose up` for Ollama to fully initialize.

### Issue: Digest returns 500 with JSON parse error
**Solution:** Verify Ollama model is downloaded (`ollama list`). The LLM may not be returning valid JSON; check Ollama logs.

### Issue: Knowledge directory empty after save
**Solution:** Check backend logs for git errors. Ensure git is installed in container (should be via Dockerfile).

### Issue: Port already in use
**Solution:**
```bash
# Find and stop conflicting services
lsof -i :8000
lsof -i :3000
lsof -i :11434
```

### Issue: Out of disk space
**Solution:** Ollama models require 5-10GB. Clean up Docker:
```bash
docker system prune -a
```

---

## Next Steps After Verification

If all tests pass:

1. **Production Deployment:**
   - Set up reverse proxy (nginx) for SSL termination
   - Configure domain names for services
   - Set up backup strategy for knowledge directory
   - Enable authentication on Open WebUI

2. **Monitoring Setup:**
   - Add healthcheck directives to docker-compose.yml
   - Set up log aggregation
   - Monitor Ollama memory usage

3. **Feature Enhancements:**
   - Add automated tests with pytest
   - Implement vector embeddings for semantic search
   - Add API authentication (JWT tokens)
   - Create backup/restore endpoints

4. **Documentation:**
   - Document actual API response times
   - Create troubleshooting runbook
   - Add example curl scripts for common workflows

---

## Estimated Time

- **Phase 1 (Startup):** 10-15 minutes (including model download)
- **Phase 2 (API Tests):** 10 minutes
- **Phase 3 (Storage):** 5 minutes
- **Phase 4 (WebUI):** 5 minutes
- **Phase 5 (Error Tests):** 5 minutes
- **Phase 6 (Performance):** 2 minutes
- **Phase 7 (Restart):** 5 minutes

**Total:** ~40-50 minutes for complete verification

---

## Conclusion

This verification plan provides systematic validation of all personal-llm-box components. Execute phases sequentially, checking off each item. Document any failures or unexpected behavior for debugging.

The system is production-ready once all success criteria are met.
